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

#ifndef SAMPLENAMESPACE_H
#define SAMPLENAMESPACE_H

#include "libsamplemacros.h"
#include "str.h"
#include "point.h"

class ObjectType;

// Anonymous global enum
enum {
    AnonymousGlobalEnum_Value0,
    AnonymousGlobalEnum_Value1
};

namespace SampleNamespace
{

enum Option {
    None,
    RandomNumber,
    UnixTime
};

enum InValue {
    ZeroIn,
    OneIn,
    TwoIn
};

enum OutValue {
    ZeroOut,
    OneOut,
    TwoOut
};

// Anonymous non-global enum.
// This counts as a class enum, since C++ namespaces
// are represented as classes in Python.
enum {
    AnonymousClassEnum_Value0,
    AnonymousClassEnum_Value1
};

LIBSAMPLE_API OutValue enumInEnumOut(InValue in);

LIBSAMPLE_API int getNumber(Option opt);

inline double powerOfTwo(double num) {
    return num * num;
}

LIBSAMPLE_API void doSomethingWithArray(const unsigned char* data, unsigned int size, const char* format = 0);

LIBSAMPLE_API int enumItemAsDefaultValueToIntArgument(int value = ZeroIn);

class SomeClass
{
public:
    class SomeInnerClass
    {
    public:
        class OkThisIsRecursiveEnough
        {
        public:
            virtual ~OkThisIsRecursiveEnough() {}
            enum NiceEnum {
                NiceValue1, NiceValue2
            };

            inline int someMethod(SomeInnerClass*) { return 0; }
            virtual OkThisIsRecursiveEnough* someVirtualMethod(OkThisIsRecursiveEnough* arg) { return arg; }
        };
    };
};

class DerivedFromNamespace : public SomeClass::SomeInnerClass::OkThisIsRecursiveEnough
{
public:
    virtual OkThisIsRecursiveEnough* someVirtualMethod(OkThisIsRecursiveEnough* arg) { return arg; }
    inline OkThisIsRecursiveEnough* methodReturningTypeFromParentScope() { return 0; }
};

// The combination of the following two overloaded methods could trigger a
// problematic behaviour on the overload decisor, if it isn't working properly.
LIBSAMPLE_API void forceDecisorSideA(ObjectType* object = 0);
LIBSAMPLE_API void forceDecisorSideA(const Point& pt, const Str& text, ObjectType* object = 0);

// The combination of the following two overloaded methods could trigger a
// problematic behaviour on the overload decisor, if it isn't working properly.
// This is a variation of forceDecisorSideB.
LIBSAMPLE_API void forceDecisorSideB(int a, ObjectType* object = 0);
LIBSAMPLE_API void forceDecisorSideB(int a, const Point& pt, const Str& text, ObjectType* object = 0);

} // namespace SampleNamespace

#endif // SAMPLENAMESPACE_H

