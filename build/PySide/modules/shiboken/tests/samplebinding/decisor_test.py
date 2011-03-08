#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of the Shiboken Python Bindings Generator project.
#
# Copyright (C) 2009 Nokia Corporation and/or its subsidiary(-ies).
#
# Contact: PySide team <contact@pyside.org>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public License
# version 2.1 as published by the Free Software Foundation. Please
# review the following information to ensure the GNU Lesser General
# Public License version 2.1 requirements will be met:
# http://www.gnu.org/licenses/old-licenses/lgpl-2.1.html.
# #
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA
# 02110-1301 USA

'''Test cases for the method overload decisor.'''

import unittest

from sample import SampleNamespace, Point

class DecisorTest(unittest.TestCase):
    '''Test cases for the method overload decisor.'''

    def testCallWithInvalidParametersSideA(self):
        '''Call a method missing with the last argument missing.
        This can trigger the bug #262, which means using an argument
        not provided by the user.'''
        pt = Point()
        self.assertRaises(TypeError, SampleNamespace.forceDecisorSideA, pt)

    def testCallWithInvalidParametersSideB(self):
        '''Same as the previous test, but with an integer as first argument,
        just to complicate things for the overload method decisor.'''
        pt = Point()
        self.assertRaises(TypeError, SampleNamespace.forceDecisorSideB, 1, pt)

if __name__ == '__main__':
    unittest.main()

