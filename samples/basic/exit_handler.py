#!/usr/bin/env python3
# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import kfp.dsl as dsl


@dsl.pipeline(
  name='Exit Handler',
  description='Download a message and print it out. Exit Handler will run at the end.'
)
def download_and_print(
  url=dsl.PipelineParam(name='url', value='gs://ml-pipeline-playground/shakespeare1.txt')):
  """A sample pipeline showing exit handler."""

  exit_op = dsl.ContainerOp(
      name='finally',
      image='library/bash:4.4.23',
      command=['echo', 'exit!'])

  with dsl.ExitHandler(exit_op):

    op1 = dsl.ContainerOp(
       name='download',
       image='google/cloud-sdk:216.0.0',
       command=['sh', '-c'],
       arguments=['gsutil cat %s | tee /tmp/results.txt' % url],
       file_outputs={'downloaded': '/tmp/results.txt'})

    op2 = dsl.ContainerOp(
       name='echo',
       image='library/bash:4.4.23',
       command=['sh', '-c'],
       arguments=['echo %s' % op1.output])

if __name__ == '__main__':
  import kfp.compiler as compiler
  compiler.Compiler().compile(download_and_print, __file__ + '.tar.gz')
