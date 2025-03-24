#! /usr/bin/env python
# coding=UTF-8

# Copyright IBM Inc. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
# Author(s): Vassilis Vassiliadis

"""Validates an experiment and prints out memoization hashes of components"""

from __future__ import print_function

import logging
import optparse
import os
import shutil
import sys
import traceback
from typing import TYPE_CHECKING

from six import string_types

import experiment.appenv
import experiment.model.conf
import experiment.model.data
import experiment.model.errors
import experiment.model.frontends.dosini
import experiment.runtime.output
import experiment.model.storage
import networkx

if TYPE_CHECKING:
    from experiment.model.data import Experiment
    from experiment.model.conf import FlowIRExperimentConfiguration
    import experiment.model

usage = "usage: %prog [options] [package]"

parser = optparse.OptionParser(usage=usage, version="% 0.1", description=__doc__)

testGroup = optparse.OptionGroup(parser, "Control the tests that will be run")
parser.add_option_group(testGroup)
available_package_types = [key for key in list(
    experiment.model.conf.ExperimentConfigurationFactory.format_map.keys()) if isinstance(key, string_types)]

parser.add_option('--printMemoInfo', dest='printMemoInfo',
                  help='Set this to always print contents of structure used to generate memoization embeddings.',
                  action="store_true",
                  default=False,
                  )
parser.add_option('-c', '--component', dest='component', help='If specified will only print information for component'
                                                              ' reference (e.g. stage0.foo)',
                  default=None)
parser.add_option('--cwlFile', dest='cwlFile',
                      help='Override cwl main file - default main.cwl',
                      default=None)
parser.add_option('--cwlJobOrderFile', dest='cwlJobOrderFile',
                      help='Override cwl job-order file. Set the option to '' to disable loading a job-order file '
                           '- default job_order.yml',
                      default=None)
parser.add_option("--formatPriority", dest="formatPriority",
                  help="Comma separated list of configuration format priorities that "
                       "guides the selection of the Configuration parser which "
                       "will be used to read the Experiment configuration (Available options: %s)."
                       " - default '%%default'" % available_package_types,
                  default=','.join(experiment.model.conf.ExperimentConfigurationFactory.default_priority)
                  )
parser.add_option("-w", "--writeStageConfs", dest="writeStageConfs",
                  help="If given the replicate stage configuration files will be written",
                  action="store_true",
                  default=False,
                  metavar="WRITE_CONFS")
parser.add_option("-p", "--platform", dest="platform",
                  help="The platform the experiment is being deployed on. No effect if etest.py is run on an instance ",
                  default=None,
                  metavar="PLATFORM")
parser.add_option("-l", "--logLevel", dest="logLevel",
                  help="The level of logging. Default %default",
                  type="int",
                  default=30,
                  metavar="LOGGING")
parser.add_option("-v", "--verbose", dest="verbose",
                  help="Turns on debugging output",
                  action="store_true",
                  default=False,
                  metavar="VERBOSE")
parser.add_option("-k", "--keepInstance", dest="keepInstance",
                  help="Keep the created instance directory",
                  action="store_true",
                  default=False,
                  metavar="KEEP_INSTANCE")
parser.add_option("", "--outputEnvironments", dest="outputEnvironments",
                     help="If specified the constructed environments are written to output",
                     action="store_true",
                     default=False,
                     metavar="OUTPUT_ENVS")
parser.add_option('', '--manifest', dest="manifest",metavar="PATH_TO_MANIFEST_FILE", default=None,
                             help="Optional path to manifest YAML file to use when setting up package directory from a "
                                  "FlowIR YAML file. The manifest should contain a dictionary, with "
                                  "targetFolder: sourceFolder entries. Each sourceFolder will be copied or linked to "
                                  "populate the respective targetFolder. Source folders can be absolute paths, or "
                                  "paths relative to the path of the FlowIR YAML file. SourceFolders may also be "
                                  "suffixed with :copy or :link to control whether targetFolder will be copied or "
                                  "linked to sourceFolder (default is copy). TargetFolders are interpreted as relative "
                                  "paths under the instance directory. They may also be the resulting folder name of "
                                  "some applicationDependency. They may include a path-separator (.e.g /) but must not "
                                  "be absolute paths.")

testGroup.add_option("", "--testHybrid", dest="testHybrid",
                  help="Perform test with hybrid environment active (temporary). "
                   "Note: The value of the env-var ETEST_REMOTE_QUEUE will be used for the remote queue if defined. ",
                  action="store_true",
                  default=False,
                  metavar="TEST_HYBRID")
testGroup.add_option("", "--notestComponents", dest="testComponents",
                  help="Don't test component references are valid",
                  action="store_false",
                  default=True,
                  metavar="TEST_REFERENCES")
testGroup.add_option("", "--testExecutables", dest="testExecutables",
                     help="Don't test if specified executables exist. "
                     "NOTE: This also turns of testing of Sandbox specifications unless testSandbox is specified",
                     action="store_true",
                     default=False,
                     metavar="TEST_EXECUTABLES")
testGroup.add_option("", "--testSandbox", dest="testSandbox",
                     help="Test sandboxing via applications when testExecutables is OFF."
                          "This only has an effect if notestExecutables was specified. "
                          "The option allows handling when the sandboxing is holding data",
                     action="store_true",
                     default=False,
                     metavar="TEST_SANDBOX")
testGroup.add_option("", "--testDirect", dest="testDirect",
                     help="Test if direct references exist. "
                     "Note this is off by default as it requires input data to pass. "
                     "This means it will always fail in this scenario (as there is no input data in the package). "
                     "However it still can be used to check if non-input direct data is present",
                     action="store_true",
                     default=False,
                     metavar="TEST_DIRECT")
parser.add_option("", "--repairShadowDir", help="Attempt to repair shadow directory (default: False)",
                      action="store_true",
                      metavar="REPAIR_SHADOW_DIR",
                      default=False)

options, args = parser.parse_args()

FORMAT = '%(levelname)-9s %(threadName)-30s %(name)-30s: %(funcName)-20s %(asctime)-15s: %(message)s'
logging.basicConfig(format=FORMAT)
rootLogger = logging.getLogger() 
rootLogger.setLevel(options.logLevel)

if len(args) != 1:
    rootLogger.warning("No experiment package given - checking if inside one")
    d = experiment.model.storage.FindExperimentTopLevel()
    if d is None:
        rootLogger.info("No experiment package given and not within one - aborting")
        sys.exit(1)
    else:
        rootLogger.info("Identified experiment package at %s" % d)
        args.append(d)

# VV: Automatically inject 'cwl' if elaunch is asked to load a cwl file or a job order file
if options.cwlFile is not None or options.cwlJobOrderFile is not None:
    if 'cwl' not in options.formatPriority:
        options.formatPriority.insert(0, 'cwl')

rootLogger.warning("TESTING CONFIGURATION FROM PACKAGE\n")

isInstance=False
configMethod = None
options.formatPriority = options.formatPriority.split(',')

directory = os.path.normpath(os.path.abspath(args[0]))

cwl_options = {}
if options.cwlFile is not None:
    cwl_options['cwlFile'] = options.cwlFile

if options.cwlJobOrderFile is not None:
    cwl_options['cwlJobOrderFile'] = options.cwlJobOrderFile

if directory.endswith('.instance'):
    isInstance = True
    experimentDirPath = os.path.abspath(directory)

    def configMethod(directory, **kwargs):
        return experiment.model.conf.ExperimentConfigurationFactory.configurationForExperiment(
            directory, createInstanceFiles=False, updateInstanceFiles=False, primitive=True,
            is_instance=isInstance, **kwargs)

    def getExperiment():
        # VV: We should be able to define a platform for packages but not for instances
        if options.platform != None:
            raise NotImplementedError("Cannot specify a platform for an instance directory (path ends in .instance)")

        return experiment.model.data.Experiment.experimentFromInstance(
            experimentDirPath, updateInstanceConfiguration=False, format_priority=options.formatPriority,
            attempt_shadowdir_repair=options.repairShadowDir
        )
else:
    def configMethod(location, format_priority, **kwargs):
        conf, _ = experiment.model.conf.ExperimentConfigurationFactory.configurationForExperiment(
            location, platform=options.platform, format_priority=format_priority,
            createInstanceFiles=False, updateInstanceFiles=False)
        return conf

    def getExperiment():
        # VV: We should be able to define a platform for packages but not for instances
        d = {'platform':options.platform, 'timestamp':False}
        if not options.testExecutables:
            d['createVirtualEnvLinks'] = False
            if not options.testSandbox:
                d['createApplicationLinks'] = False

        #Use /tmp is availale
        if os.path.exists('/tmp'):
            d['location'] = '/tmp'

        d.update(cwl_options)

        experimentPackage = experiment.model.storage.ExperimentPackage.packageFromLocation(
            directory, manifest=options.manifest, platform=options.manifest)
        return experiment.model.data.Experiment.experimentFromPackage(experimentPackage, **d)

e = None

if options.testHybrid:
    remoteQueue = os.environ['ETEST_REMOTE_QUEUE'] if 'ETEST_REMOTE_QUEUE' in os.environ else "test-queue"
    rootLogger.info('Hybrid environment on. Using %s as the remote queue' % remoteQueue)
    experiment.appenv.HybridConfiguration.newDefaultConfiguration(isHybrid=True, remoteQueue=remoteQueue)

try:    
    #Create configuration
    c = configMethod(
        directory, format_priority=options.formatPriority, **cwl_options
    )  # type: FlowIRExperimentConfiguration

    # VV: @tag:DeprecateThis
    if options.writeStageConfs is True:
        rootLogger.warning("WRITING REPLICATED STAGE CONFIGURATIONS")
        for i in range(c.numberStageConfigurations):

            with open("stage%d.conf" % i, "w") as f:
                s = c.configurationForStage(i)
                s.write(f)

    if options.outputEnvironments is True:
        with open("constructed_environments.txt", "w") as f:
            for env in c.constructedEnvironments:
                f.write('\n')
                f.write('CONSTRUCTED ENVIRONMENT: %s\n' % env)
                env = c.environmentWithName(env)
                for k in list(env.keys()):
                    f.write("%s=%s\n" % (k, env[k]))

            f.write('CONSTRUCTED ENVIRONMENT: Global')
            env = c.defaultEnvironment()
            for k in list(env.keys()):
                f.write("%s=%s\n" % (k, env[k]))

    rootLogger.warning("TESTING EXPERIMENT FROM PACKAGE\n")

    e = getExperiment()  # type: Experiment
    import pprint

    def print_intended(doc, prefix):
        if doc:
            doc = pprint.pformat(doc).splitlines()
            doc = ('\n%s' % prefix).join(doc)
        print('%s%s' % (prefix, doc))

    def print_memo_for_component(comp_name):
        data = e.graph.nodes[comp_name]
        spec = data['componentSpecification']  # type: "experiment.graph.ComponentSpecification"

        print(spec.identification.identifier)
        # VV: Print a trimmed view of commandDetails and references
        details = spec.commandDetails
        details['references'] = spec.rawDataReferences
        details['image'] = spec.resourceManager['kubernetes']['image']
        remove_keys = ['expandArguments', 'resolvePath', 'environment']
        for k in list(details):
            try:
                if k in remove_keys or not details[k]:
                    del details[k]
            except Exception:
                pass

        print_intended(details, '  ')

        print("  Memoization strong: %s fuzzy: %s" % (
            spec.memoization_hash, spec.memoization_hash_fuzzy
        ))

        if spec.memoization_hash_fuzzy == spec.memoization_hash:
            print("  Memoization strong is identical to fuzzy")

        if options.printMemoInfo:
            print("  contents of strong memoization info")
            print_intended(spec.memoization_info, '    ')
            if spec.memoization_hash_fuzzy != spec.memoization_hash:
                print("  contents of fuzzy memoization info")
                print_intended(spec.memoization_info_fuzzy, '    ')

    if options.component is None:
        for comp_name in networkx.topological_sort(e.graph):
            print_memo_for_component(comp_name)
    else:
        print_memo_for_component(options.component)

    e.validateExperiment(checkComponentReferences=options.testComponents,
                         checkDataReferences=options.testComponents,
                         checkExecutables=options.testExecutables,
                         checkDirectReferences=options.testDirect)

    rootLogger.warning("CHECKING ENVIRONMENTS\n")

    env = e.configuration.defaultEnvironment()
    envList = ["%s:%s" % (k, env[k]) for k in list(env.keys())]
    if len(" ".join(envList)) > 4096:
        rootLogger.warning(
            'Global environment for is greater than 4096 characters. This may cause issues. Consider reducing size.')

    for s in e.stages():
        for j in s.jobs():
            try:
                envName = e.configuration.getOptionForNode(j.identification.identifier, '#command.environment')
                if envName == "none":
                    rootLogger.warning(
                        'Empty environment explicitly specified for %s' % j.name)
                else:
                    env = e.configuration.environmentWithName(envName)
                    envList = ["%s:%s" % (k, env[k]) for k in list(env.keys())]
                    if len(" ".join(envList)) > 4096:
                        rootLogger.warning(
                            'Environment for %s (%s) is greater than 4096 characters. This may cause issues' % (
                            j.name, envName))
            except KeyError:
                rootLogger.warning(
                    'No environment specified for %s. Global experiment environment will be used' % j.name)
except experiment.model.errors.ExperimentInvalidConfigurationError as error:
    rootLogger.log(19, traceback.format_exc())
    underlying = error.underlyingError

    if isinstance(underlying, list):
        rootLogger.critical("Encountered when loading configuration:")
        for err in underlying:
            rootLogger.critical("  %s: %s" % (type(err), str(err)))
        rootLogger.critical("Discovered %d experiment configuration errors" % len(underlying))
    else:
        rootLogger.critical("Encountered error when loading configuration: %s" % underlying)
except Exception as err:
    rootLogger.log(19, traceback.format_exc())
    rootLogger.warning("Exception: %s" % err)
finally:
    if e is not None:
        # VV: Only consolidate and consider deleting the instanceDirectory if we started from a package
        #     i.e. we created the instance directory as a means to check the package
        #     if we're testing out whether an instance is correct we should leave the files on the disk

        if isInstance is True:
            rootLogger.warning("Testing instance directory %s has finished" % e.instanceDirectory.location)
        else:
            e.instanceDirectory.consolidate()
            if not options.keepInstance:
                rootLogger.warning("TEARING DOWN TEST DIRECTORIES")
                try:
                    shutil.rmtree(e.instanceDirectory.location)
                except:
                    pass
