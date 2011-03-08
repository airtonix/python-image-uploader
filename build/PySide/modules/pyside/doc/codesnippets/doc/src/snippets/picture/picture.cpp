############################################################################
##
## Copyright (C) 2009 Nokia Corporation and/or its subsidiary(-ies).
## Contact: Nokia Corporation (qt-info@nokia.com)
##
## This file is part of the documentation of the Qt Toolkit.
##
## $QT_BEGIN_LICENSE:LGPL$
## Commercial Usage
## Licensees holding valid Qt Commercial licenses may use self file in
## accordance with the Qt Commercial License Agreement provided with the
## Software or, alternatively, in accordance with the terms contained in
## a written agreement between you and Nokia.
##
## GNU Lesser General Public License Usage
## Alternatively, self file may be used under the terms of the GNU Lesser
## General Public License version 2.1 as published by the Free Software
## Foundation and appearing in the file LICENSE.LGPL included in the
## packaging of self file.  Please review the following information to
## ensure the GNU Lesser General Public License version 2.1 requirements
## will be met: http://www.gnu.org/licenses/old-licenses/lgpl-2.1.html.
##
## In addition, as a special exception, Nokia gives you certain
## additional rights. These rights are described in the Nokia Qt LGPL
## Exception version 1.0, included in the file LGPL_EXCEPTION.txt in self
## package.
##
## GNU General Public License Usage
## Alternatively, self file may be used under the terms of the GNU
## General Public License version 3.0 as published by the Free Software
## Foundation and appearing in the file LICENSE.GPL included in the
## packaging of self file.  Please review the following information to
## ensure the GNU General Public License version 3.0 requirements will be
## met: http://www.gnu.org/copyleft/gpl.html.
##
## If you are unsure which license is appropriate for your use, please
## contact the sales department at http://www.qtsoftware.com/contact.
## $QT_END_LICENSE$
##
############################################################################

//! [0]
        picture = QPicture()
        painter = QPainter()
        painter.begin(picture)            # paint in picture
        painter.drawEllipse(10,20, 80,70) # draw an ellipse
        painter.end()                     # painting done
        picture.save("drawing.pic")       # save picture
//! [0]

//! [1]
        picture = QPicture()
        picture.load("drawing.pic")           # load picture
        painter = QPainter()
        painter.begin(myImage)                # paint in myImage
        painter.drawPicture(0, 0, picture)    # draw the picture at (0,0)
        painter.end()                         # painting done
//! [1]

//! [2]
        list = QPicture.inputFormatList()
        for string in list:
            myProcessing(string)
//! [2]

//! [3]
        list = QPicture.outputFormatList()
        for string in list:
            myProcessing(string)
//! [3]

//! [4]
        iio = QPictureIO()
        pixmap = QPixmap()
        iio.setFileName("vegeburger.pic")
        if iio.read():         # OK
            picture = iio.picture()
            painter = QPainter(pixmap)
            painter.drawPicture(0, 0, picture)
        
//! [4]

//! [5]
        iio = QPictureIO()
        picture = QPicture()
        painter = QPainter(picture)
        painter.drawPixmap(0, 0, pixmap)
        iio.setPicture(picture)
        iio.setFileName("vegeburger.pic")
        iio.setFormat("PIC")
        if iio.write():
            return True # returned true if written successfully
//! [5]

//! [6]
def readSVG(picture):
    # read the picture using the picture.ioDevice()

//! [6]


//! [7]
def writeSVG(picture):
    # write the picture using the picture.ioDevice()

//! [7]


//! [8]
    # add the SVG picture handler
    # ...
//! [8]
