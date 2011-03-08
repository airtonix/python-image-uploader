#!/usr/bin/python
'''Test cases for QFlags'''

import unittest
from PySide.QtCore import *

class QFlagTest(unittest.TestCase):
    '''Test case for usage of flags'''

    def testCallFunction(self):
        f = QTemporaryFile()
        self.assert_(f.open())
        fileName = f.fileName()
        f.close()

        f = QFile(fileName)
        self.assertEqual(f.open(QIODevice.Truncate | QIODevice.Text | QIODevice.ReadWrite), True)
        om = f.openMode()
        self.assertEqual(om & QIODevice.Truncate, QIODevice.Truncate)
        self.assertEqual(om & QIODevice.Text, QIODevice.Text)
        self.assertEqual(om & QIODevice.ReadWrite, QIODevice.ReadWrite)
        self.assert_(om == QIODevice.Truncate | QIODevice.Text | QIODevice.ReadWrite)
        f.close()


class QFlagOperatorTest(unittest.TestCase):
    '''Test case for operators in QFlags'''

    def testInvert(self):
        '''QFlags ~ (invert) operator'''
        self.assertEqual(type(~QIODevice.ReadOnly), QIODevice.OpenMode)

    def testOr(self):
        '''QFlags | (or) operator'''
        self.assertEqual(type(QIODevice.ReadOnly | QIODevice.WriteOnly), QIODevice.OpenMode)

    def testAnd(self):
        '''QFlags & (and) operator'''
        self.assertEqual(type(QIODevice.ReadOnly & QIODevice.WriteOnly), QIODevice.OpenMode)

    def testIOr(self):
        '''QFlags |= (ior) operator'''
        flag = Qt.WindowFlags()
        self.assert_(flag & Qt.Widget == 0)
        flag |= Qt.WindowMinimizeButtonHint
        self.assert_(flag & Qt.WindowMinimizeButtonHint)

    def testInvertOr(self):
        '''QFlags ~ (invert) operator over the result of an | (or) operator'''
        self.assertEqual(type(~(Qt.ItemIsSelectable | Qt.ItemIsEditable)), Qt.ItemFlags)

    def testEqual(self):
        '''QFlags == operator'''
        flags = Qt.Window
        flags |= Qt.WindowMinimizeButtonHint
        flag_type = (flags & Qt.WindowType_Mask)
        self.assertEqual(flag_type, Qt.Window)

    def testOperatorBetweenFlags(self):
        '''QFlags & QFlags'''
        flags = Qt.NoItemFlags | Qt.ItemIsUserCheckable
        newflags = Qt.NoItemFlags | Qt.ItemIsUserCheckable
        self.assert_(flags & newflags)

    def testOperatorDifferentOrder(self):
        '''Different ordering of arguments'''
        flags = Qt.NoItemFlags | Qt.ItemIsUserCheckable
        self.assertEqual(flags | Qt.ItemIsEnabled, Qt.ItemIsEnabled | flags)

class QFlagsOnQVariant(unittest.TestCase):
    def testQFlagsOnQVariant(self):
        o = QObject()
        o.setProperty("foo", QIODevice.ReadOnly | QIODevice.WriteOnly)
        self.assertEqual(type(o.property("foo")), int)

class QFlagsWrongType(unittest.TestCase):
    def testWrongType(self):
        '''Wrong type passed to QFlags binary operators'''
        self.assertRaises(TypeError, lambda :Qt.NoItemFlags | '43')
        self.assertRaises(TypeError, lambda :Qt.NoItemFlags & '43')
        self.assertRaises(TypeError, lambda :'jabba' & Qt.NoItemFlags)
        self.assertRaises(TypeError, lambda :'hut' & Qt.NoItemFlags)
        self.assertRaises(TypeError, lambda :Qt.NoItemFlags & QObject())

if __name__ == '__main__':
    unittest.main()
