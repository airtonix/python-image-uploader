
import os
import unittest

from PySide import QtCore
from PySide import phonon

from helper import UsesQCoreApplication

# XXX Hack to get the correct filename
example_file = os.path.join(os.path.dirname(__file__),'tone.ogg')

class TestSimplePlaying(UsesQCoreApplication):
    def setUp(self):
        super(TestSimplePlaying, self).setUp()
        self.app.setApplicationName('Dummy')
        self.source = phonon.Phonon.MediaSource(example_file)
        self.media = phonon.Phonon.MediaObject()
        self.media.setCurrentSource(self.source)

        QtCore.QObject.connect(self.media,
                QtCore.SIGNAL('finished()'),
                self.app,
                QtCore.SLOT('quit()'))

        self.called = False

        # prevent locking with:
        # request to play a stream, but no valid audio ...
        self.output = phonon.Phonon.AudioOutput()
        self.path = phonon.Phonon.createPath(self.media, self.output)

    def tearDown(self):
        super(TestSimplePlaying, self).tearDown()
        del self.path
        del self.output
        del self.media
        del self.source

    def testFinishedSignal(self):
        # Should pass if finished() is called
        self.media.play()
        self.app.exec_()

    def testMediaSource(self):
        self.assertEqual(self.media.currentSource(), self.source)

    def testPathCreation(self):
        # FIXME Both functions below are not exported by PyQt4
        self.assertEqual(self.path.sink(), self.output)
        self.assertEqual(self.path.source(), self.media)

    def state_cb(self, newState, OldState):
        self.called = True

    def testStateChanged(self):
        # Check for ogg support before playing it
        if (phonon.Phonon.BackendCapabilities.isMimeTypeAvailable('audio/ogg')):
            QtCore.QObject.connect(self.media,
                QtCore.SIGNAL('stateChanged(Phonon::State, Phonon::State)'),
                self.state_cb)

            self.media.play()
            self.app.exec_()
            self.assert_(self.called)
        else:
            print 'Ogg format not supported! Playback test skipped!'

if __name__ == '__main__':
    unittest.main()
