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

#ifndef REFERENCE_H
#define REFERENCE_H

#include "libsamplemacros.h"

class LIBSAMPLE_API Reference
{
public:
    explicit Reference(int objId = -1)
            : m_objId(objId) {}
    virtual ~Reference() {}

    inline int objId() { return m_objId; }
    inline void setObjId(int objId) { m_objId = objId; }

    inline static int usesReference(Reference& r) { return r.m_objId; }
    inline static int usesConstReference(const Reference& r) { return r.m_objId; }

    virtual int usesReferenceVirtual(Reference& r, int inc);
    virtual int usesConstReferenceVirtual(const Reference& r, int inc);

    int callUsesReferenceVirtual(Reference& r, int inc);
    int callUsesConstReferenceVirtual(const Reference& r, int inc);

    virtual void alterReferenceIdVirtual(Reference& r);
    void callAlterReferenceIdVirtual(Reference& r);

    void show() const;

    inline static int multiplier() { return 10; }

private:
    int m_objId;
};

#endif // REFERENCE_H

