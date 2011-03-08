#!/usr/bin/python
# -*- coding: utf-8 -*-

'''Unit tests to test QTranslator and translation in general.'''

import os
import glob
import unittest
from PySide.QtCore import *

from helper import UsesQCoreApplication

class TranslationTest(UsesQCoreApplication):
    '''Test case for Qt translation facilities.'''

    def setUp(self):
        super(TranslationTest, self).setUp()
        self.trdir = os.path.join(os.path.dirname(__file__), 'translations')
        # os.system is probably not the best way to do it
	for file in glob.glob('%s/*.ts'  % self.trdir):
	    self.assertFalse(os.system('lrelease -silent %s' % file))

    def tearDown(self):
	for file in glob.glob('%s/*.qm'  % self.trdir):
	    os.remove(file)
        super(TranslationTest, self).tearDown()

    def testLatin(self):
        #Set string value to Latin
        translator = QTranslator()
        translator.load(os.path.join(self.trdir, 'trans_latin.qm'))
        self.app.installTranslator(translator)

        obj = QObject()
        obj.setObjectName(obj.tr('Hello World!'))
        self.assertEqual(obj.objectName(), u'Orbis, te saluto!')

    def testRussian(self):
        #Set string value to Russian
        translator = QTranslator()
        translator.load(os.path.join(self.trdir, 'trans_russian.qm'))
        self.app.installTranslator(translator)

        obj = QObject()
        obj.setObjectName(obj.tr('Hello World!'))
        self.assertEqual(obj.objectName(), u'привет мир!')

    def testUtf8(self):
        translator = QTranslator()
        translator.load(os.path.join(self.trdir, 'trans_russian.qm'))
        self.app.installTranslator(translator)

        obj = QObject()
        obj.setObjectName(obj.trUtf8('Hello World!'))
        self.assertEqual(obj.objectName(), u'привет мир!')

    def testTranslateWithNoneDisambiguation(self):
        value = 'String here'
        obj = QCoreApplication.translate('context', value, None, QCoreApplication.UnicodeUTF8)
        self.assert_(isinstance(obj, unicode))
        self.assertEqual(obj, value)

if __name__ == '__main__':
    unittest.main()

