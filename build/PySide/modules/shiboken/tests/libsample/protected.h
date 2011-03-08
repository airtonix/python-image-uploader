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

#ifndef PROTECTED_H
#define PROTECTED_H

#include "libsamplemacros.h"
#include <string>

class ProtectedNonPolymorphic
{
public:
    explicit ProtectedNonPolymorphic(const char *name) : m_name(name) {}
    ~ProtectedNonPolymorphic() {}

    inline const char* publicName() { return m_name.c_str(); }

    inline static ProtectedNonPolymorphic* create() { return new ProtectedNonPolymorphic("created"); }

protected:
    inline const char* protectedName() { return m_name.c_str(); }
    inline int protectedSum(int a0, int a1) { return a0 + a1; }
    inline int modifiedProtectedSum(int a0, int a1) { return a0 + a1; }
    inline static const char* protectedStatic() { return "protectedStatic"; }
    inline const char* dataTypeName(void *data = 0) const { return "pointer"; }
    inline const char* dataTypeName(int data) const { return "integer"; }

private:
    std::string m_name;
};

class ProtectedPolymorphic
{
public:
    explicit ProtectedPolymorphic(const char *name) : m_name(name) {}
    virtual ~ProtectedPolymorphic() {}

    inline static ProtectedPolymorphic* create() { return new ProtectedPolymorphic("created"); }
    inline const char* publicName() { return m_name.c_str(); }
    inline const char* callProtectedName() { return protectedName(); }

protected:
    virtual const char* protectedName() { return m_name.c_str(); }

private:
    std::string m_name;
};

class ProtectedPolymorphicDaughter : public ProtectedPolymorphic
{
public:
    explicit ProtectedPolymorphicDaughter(const char *name) : ProtectedPolymorphic(name) {}
    inline static ProtectedPolymorphicDaughter* create() { return new ProtectedPolymorphicDaughter("created"); }
};

class ProtectedPolymorphicGrandDaughter: public ProtectedPolymorphicDaughter
{
public:
    explicit ProtectedPolymorphicGrandDaughter(const char *name) : ProtectedPolymorphicDaughter(name) {}
    inline static ProtectedPolymorphicGrandDaughter* create() { return new ProtectedPolymorphicGrandDaughter("created"); }
};

class LIBSAMPLE_API ProtectedVirtualDestructor
{
public:
    ProtectedVirtualDestructor() {}
    inline static ProtectedVirtualDestructor* create() { return new ProtectedVirtualDestructor(); }
    inline static int dtorCalled() { return dtor_called; }
    inline static void resetDtorCounter() { dtor_called = 0; }
protected:
    virtual ~ProtectedVirtualDestructor() { dtor_called++; }
private:
    static int dtor_called;
};

class ProtectedEnumClass
{
public:
    ProtectedEnumClass() {}
    virtual ~ProtectedEnumClass() {}
    enum PublicEnum {
        PublicItem0,
        PublicItem1
    };
protected:
    enum ProtectedEnum {
        ProtectedItem0,
        ProtectedItem1
    };
    ProtectedEnum callProtectedEnumMethod(ProtectedEnum in) { return protectedEnumMethod(in); }
    inline PublicEnum callPublicEnumMethod(PublicEnum in) { return publicEnumMethod(in); }

    virtual ProtectedEnum protectedEnumMethod(ProtectedEnum in) { return in; }
    virtual PublicEnum publicEnumMethod(PublicEnum in) { return in; }
};


class ProtectedProperty
{
public:
    ProtectedProperty() : protectedProperty(0) {}
protected:
    int protectedProperty;
};

#endif // PROTECTED_H

