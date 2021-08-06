#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (C) 1998-2021 Stephane Galland <galland@arakhne.org>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 59 Temple Place - Suite 330,
# Boston, MA 02111-1307, USA.


import unittest
import logging

from autolatex2.utils.runner import *

class TestAbstractRunner(unittest.TestCase):

	def setUp(self):
		logging.getLogger().setLevel(logging.CRITICAL)



	def test_runPython_valid1(self):
		(sout, serr, sex, retcode) = AbstractRunner.runPython('myvar = \'abc\'')
		self.assertEqual('', sout)
		self.assertEqual('', serr)
		self.assertIsNone(sex)
		self.assertEqual(0, retcode)

	def test_runPython_valid2(self):
		(sout, serr, sex, retcode) = AbstractRunner.runPython('myvar = \'abc\'\nprint(myvar)')
		self.assertEqual('abc\n', sout)
		self.assertEqual('', serr)
		self.assertIsNone(sex)
		self.assertEqual(0, retcode)

	def test_runPython_valid3(self):
		(sout, serr, sex, retcode) = AbstractRunner.runPython('myvar = \'abc\'\nsys.stderr.write(myvar)')
		self.assertEqual('', sout)
		self.assertEqual('abc', serr)
		self.assertIsNone(sex)
		self.assertEqual(0, retcode)

	def test_runPython_valid4(self):
		with self.assertRaises(NotImplementedError):
			AbstractRunner.runPython('raise NotImplementedError')

	def test_runPython_valid5(self):
		with self.assertRaises(NotImplementedError):
			AbstractRunner.runPython('raise NotImplementedError', False)

	def test_runPython_valid6(self):
		(sout, serr, sex, retcode) = AbstractRunner.runPython('raise NotImplementedError', True)
		self.assertEqual('', sout)
		self.assertEqual('', serr)
		self.assertIsInstance(sex, NotImplementedError)
		self.assertNotEqual(0, retcode)

	def test_runPython_invalid1(self):
		with self.assertRaises(SyntaxError):
			AbstractRunner.runPython('print(1')

	def test_runPython_invalid2(self):
		with self.assertRaises(SyntaxError):
			AbstractRunner.runPython('print(1', False)

	def test_runPython_invalid3(self):
		(sout, serr, sex, retcode) = AbstractRunner.runPython('print(1', True)
		self.assertEqual('', sout)
		self.assertEqual('', serr)
		self.assertIsInstance(sex, SyntaxError)
		self.assertNotEqual(0, retcode)



	def test_runCommand_valid1(self):
		(sout, serr, sex, retcode) = AbstractRunner.runCommand('python', '-c', 'print 123')
		self.assertEqual('123\n', sout)
		self.assertEqual('', serr)
		self.assertIsNone(sex)
		self.assertEqual(0, retcode)

	def test_runCommand_valid2(self):
		(sout, serr, sex, retcode) = AbstractRunner.runCommand('python', '-c', 'import sys;sys.stderr.write(\'123\\n\')')
		self.assertEqual('', sout)
		self.assertEqual('123\n', serr)
		self.assertIsNone(sex)
		self.assertEqual(0, retcode)

	def test_runCommand_invalid1(self):
		(sout, serr, sex, retcode) = AbstractRunner.runCommand('python', '-c', 'sys.stderr.write(\'123\\n\')')
		self.assertEqual('', sout)
		self.assertEqual('Traceback (most recent call last):\n  File "<string>", line 1, in <module>\nNameError: name \'sys\' is not defined\n', serr)
		self.assertIsInstance(sex, CommandExecutionError)
		self.assertNotEqual(0, sex.errno)
		self.assertNotEqual(0, retcode)
		self.assertEqual(sex.errno, retcode)




	def test_runScript_valid1(self):
		script = 'print 123'
		(sout, serr, sex, retcode) = AbstractRunner.runScript(script, 'python', '-')
		self.assertEqual('123\n', sout)
		self.assertEqual('', serr)
		self.assertIsNone(sex)
		self.assertEqual(0, retcode)

	def test_runScript_valid2(self):
		script = 'import sys;sys.stderr.write(\'123\\n\')'
		(sout, serr, sex, retcode) = AbstractRunner.runScript(script, 'python', '-')
		self.assertEqual('', sout)
		self.assertEqual('123\n', serr)
		self.assertIsNone(sex)
		self.assertEqual(0, retcode)

	def test_runScript_invalid1(self):
		script = 'sys.stderr.write(\'123\\n\')'
		(sout, serr, sex, retcode) = AbstractRunner.runScript(script, 'python', '-')
		self.assertEqual('', sout)
		self.assertEqual('Traceback (most recent call last):\n  File "<stdin>", line 1, in <module>\nNameError: name \'sys\' is not defined\n', serr)
		self.assertIsInstance(sex, CommandExecutionError)
		self.assertNotEqual(0, sex.errno)
		self.assertNotEqual(0, retcode)
		self.assertEqual(sex.errno, retcode)




if __name__ == '__main__':
    unittest.main()

