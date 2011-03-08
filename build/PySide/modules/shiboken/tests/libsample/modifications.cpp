/*
 * This file is part of the Shiboken Python Binding Generator project.
 *
 * Copyright (C) 2009 Nokia Corporation and/or its subsidiary(-ies).
 *
 * Contact: PySide team <contact@pyside.org>
 *
 * This library is free software; you can redistribute it and/or
 * modify it under the terms of the GNU Lesser General Public
 * License as published by the Free Software Foundation; either
 * version 2.1 of the License, or (at your option) any later version.
 *
 * This library is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 * Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public
 * License along with this library; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
 */

#include <iostream>
#include "modifications.h"

using namespace std;

std::pair<double, double>
Modifications::pointToPair(Point pt, bool* ok)
{
    std::pair<double, double> retval(pt.x(), pt.y());
    *ok = true;
    return retval;
}

double
Modifications::multiplyPointCoordsPlusValue(bool* ok, Point pt, double value)
{
    double retval = (pt.x() * pt.y()) + value;
    *ok = true;
    return retval;
}

int
Modifications::doublePlus(int value, int plus)
{
    return (2 * value) + plus;
}

int
Modifications::power(int base, int exponent)
{
    if (exponent == 0)
        return 1;
    int retval = base;
    for (int i = 1; i < exponent; i++)
        retval = retval * base;
    return retval;
}

int
Modifications::timesTen(int number)
{
    return number * 10;
}

int
Modifications::increment(int number)
{
    return ++number;
}

void
Modifications::exclusiveCppStuff()
{
    cout << __FUNCTION__ << endl;
}

int
Modifications::cppMultiply(int a, int b)
{
    return a * b;
}

const char*
Modifications::className()
{
    return "Modifications";
}

