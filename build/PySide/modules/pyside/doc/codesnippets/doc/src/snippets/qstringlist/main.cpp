/****************************************************************************
**
** Copyright (C) 2009 Nokia Corporation and/or its subsidiary(-ies).
** Contact: Nokia Corporation (qt-info@nokia.com)
**
** This file is part of the documentation of the Qt Toolkit.
**
** $QT_BEGIN_LICENSE:LGPL$
** Commercial Usage
** Licensees holding valid Qt Commercial licenses may use this file in
** accordance with the Qt Commercial License Agreement provided with the
** Software or, alternatively, in accordance with the terms contained in
** a written agreement between you and Nokia.
**
** GNU Lesser General Public License Usage
** Alternatively, this file may be used under the terms of the GNU Lesser
** General Public License version 2.1 as published by the Free Software
** Foundation and appearing in the file LICENSE.LGPL included in the
** packaging of this file.  Please review the following information to
** ensure the GNU Lesser General Public License version 2.1 requirements
** will be met: http://www.gnu.org/licenses/old-licenses/lgpl-2.1.html.
**
** In addition, as a special exception, Nokia gives you certain
** additional rights. These rights are described in the Nokia Qt LGPL
** Exception version 1.0, included in the file LGPL_EXCEPTION.txt in this
** package.
**
** GNU General Public License Usage
** Alternatively, this file may be used under the terms of the GNU
** General Public License version 3.0 as published by the Free Software
** Foundation and appearing in the file LICENSE.GPL included in the
** packaging of this file.  Please review the following information to
** ensure the GNU General Public License version 3.0 requirements will be
** met: http://www.gnu.org/copyleft/gpl.html.
**
** If you are unsure which license is appropriate for your use, please
** contact the sales department at http://www.qtsoftware.com/contact.
** $QT_END_LICENSE$
**
****************************************************************************/

#include <QtGui>
#include <iostream>
using namespace std

class Widget : public QWidget
{
public:
    Widget(QWidget *parent = 0)
}

Widget::Widget(QWidget *parent)
    : QWidget(parent)
{
//! [0]
    fonts = QStringList()
    fonts << "Arial" << "Helvetica" << "Times" << "Courier"
//! [0]

//! [1]
    for i in range(fonts.size()):
         print fonts.at(i)
//! [1]

//! [2]
    QStringListIterator javaStyleIterator(fonts)
    while (javaStyleIterator.hasNext())
         cout << javaStyleIterator.next().toLocal8Bit().constData() << endl
//! [2]

//! [3]
    QStringList::const_iterator constIterator
    for (constIterator = fonts.constBegin(); constIterator != fonts.constEnd()
           ++constIterator)
        cout << (*constIterator).toLocal8Bit().constData() << endl
//! [3]

//! [4]
    str = fonts.join(",")
     # str == "Arial,Helvetica,Times,Courier"
//! [4]

//! [5] //! [6]
    list = QStringList()
//! [5]
    list = str.split(",")
     # list: ["Arial", "Helvetica", "Times", "Courier"]
//! [6]

//! [7]
    monospacedFonts = fonts.filter(QRegExp("Courier|Fixed"))
//! [7]

//! [8]
    files = QStringList()
    files << "$QTDIR/src/moc/moc.y" \
          << "$QTDIR/src/moc/moc.l" \
          << "$QTDIR/include/qconfig.h" \

    files.replaceInStrings("$QTDIR", "/usr/lib/qt")
    # files: [ "/usr/lib/qt/src/moc/moc.y", ...]
//! [8]

    QString str1, str2, str3
//! [9]
    longerList = (QStringList() << str1 << str2 << str3)
//! [9]

    list.clear()
//! [10]
    list << "Bill Murray" << "John Doe" << "Bill Clinton"

//! [11]
    result = QStringList()
//! [11]
    result = list.filter("Bill")
    # result: ["Bill Murray", "Bill Clinton"]
//! [10]

    result.clear()
//! [12]
    for string in list:
        if string.contains("Bill")
            result += string
//! [12]

    list.clear()
//! [13]
    list << "alpha" << "beta" << "gamma" << "epsilon"
    list.replaceInStrings("a", "o")
    # list == ["olpho", "beto", "gommo", "epsilon"]
//! [13]

    list.clear()
//! [14]
    list << "alpha" << "beta" << "gamma" << "epsilon"
    list.replaceInStrings(QRegExp("^a"), "o")
    # list == ["olpha", "beta", "gamma", "epsilon"]
//! [14]

    list.clear()
//! [15]
    list << "Bill Clinton" << "Murray, Bill"
    list.replaceInStrings(QRegExp("^(.*), (.*)$"), "\\2 \\1")
    # list == ["Bill Clinton", "Bill Murray"]
//! [15]
}

int main(int argc, char *argv[])
{
    QApplication app(argc, argv)
    Widget widget
    widget.show()
    return app.exec()
}
