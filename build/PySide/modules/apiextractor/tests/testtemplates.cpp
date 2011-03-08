/*
* This file is part of the API Extractor project.
*
* Copyright (C) 2009 Nokia Corporation and/or its subsidiary(-ies).
*
* Contact: PySide team <contact@pyside.org>
*
* This program is free software; you can redistribute it and/or
* modify it under the terms of the GNU General Public License
* version 2 as published by the Free Software Foundation.
*
* This program is distributed in the hope that it will be useful, but
* WITHOUT ANY WARRANTY; without even the implied warranty of
* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
* General Public License for more details.
*
* You should have received a copy of the GNU General Public License
* along with this program; if not, write to the Free Software
* Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA
* 02110-1301 USA
*
*/

#include "testtemplates.h"
#include <QtTest/QTest>
#include <QTemporaryFile>
#include "testutil.h"

void TestTemplates::testTemplateWithNamespace()
{
    const char cppCode[] = "\
    struct Url {\
      void name();\
    };\
    namespace Internet {\
        struct Url{};\
        struct Bookmarks {\
            QList<Url> list();\
        };\
    }";
    const char xmlCode0[] = "\
    <typesystem package='Pakcage.Network'>\
        <value-type name='Url' />\
    </typesystem>";

    QTemporaryFile file;
    QVERIFY(file.open());
    file.write(xmlCode0);
    file.close();

    QString xmlCode1 = QString("\
    <typesystem package='Package.Internet'>\
        <load-typesystem name='%1' generate='no'/>\
        <container-type name='QList' type='list'/> \
        <namespace-type name='Internet' generate='no' />\
        <value-type name='Internet::Url'/>\
        <value-type name='Internet::Bookmarks'/>\
    </typesystem>").arg(file.fileName());

    TestUtil t(cppCode, qPrintable(xmlCode1), false);
    AbstractMetaClassList classes = t.builder()->classes();

    AbstractMetaClass* classB = classes.findClass("Bookmarks");
    QVERIFY(classB);
    const AbstractMetaFunction* func = classB->findFunction("list");
    AbstractMetaType* funcType = func->type();
    QVERIFY(funcType);
    QCOMPARE(funcType->cppSignature(), QString("QList<Internet::Url >"));
}

void TestTemplates::testTemplateOnContainers()
{
    const char cppCode[] = "\
    struct Base {};\
    namespace Namespace {\
    enum SomeEnum { E1, E2 };\
    template<SomeEnum type> struct A {\
        A<type> foo(const QList<A<type> >& a);\
    };\
    typedef A<E1> B;\
    }\
    ";
    const char xmlCode[] = "\
    <typesystem package=\"Package\">\
        <container-type name='QList' type='list'/> \
        <namespace-type name='Namespace' />\
        <enum-type name='Namespace::SomeEnum'/>\
        <object-type name='Base' />\
        <object-type name='Namespace::A' generate='no'/> \
        <object-type name='Namespace::B'/> \
    </typesystem>";

    TestUtil t(cppCode, xmlCode, false);
    AbstractMetaClassList classes = t.builder()->classes();

    AbstractMetaClass* classB = classes.findClass("B");
    QVERIFY(!classB->baseClass());
    QVERIFY(classB->baseClassName().isNull());
    const AbstractMetaFunction* func = classB->findFunction("foo");
    AbstractMetaType* argType = func->arguments().first()->type();
    QCOMPARE(argType->instantiations().count(), 1);
    QCOMPARE(argType->typeEntry()->qualifiedCppName(), QString("QList"));

    const AbstractMetaType* instance1 = argType->instantiations().first();
    QCOMPARE(instance1->instantiations().count(), 1);
    QCOMPARE(instance1->typeEntry()->qualifiedCppName(), QString("Namespace::A"));

    const AbstractMetaType* instance2 = instance1->instantiations().first();
    QCOMPARE(instance2->instantiations().count(), 0);
    QCOMPARE(instance2->typeEntry()->qualifiedCppName(), QString("Namespace::E1"));
}

void TestTemplates::testInheritanceFromContainterTemplate()
{
    const char cppCode[] = "\
    template<typename T>\
    struct ListContainer {\
        inline void push_front(const T& t);\
        inline T& front();\
    };\
    struct FooBar {};\
    struct FooBars : public ListContainer<FooBar> {};\
    ";

    const char xmlCode[] = "\
    <typesystem package='Package'>\
        <container-type name='ListContainer' type='list' /> \
        <value-type name='FooBar' />\
        <value-type name='FooBars'>\
            <modify-function signature='push_front(FooBar)' remove='all' />\
            <modify-function signature='front()' remove='all' />\
        </value-type>\
    </typesystem>\
    ";

    TestUtil t(cppCode, xmlCode, false);
    AbstractMetaClassList classes = t.builder()->classes();
    AbstractMetaClassList templates = t.builder()->templates();
    QCOMPARE(classes.count(), 2);
    QCOMPARE(templates.count(), 1);

    const AbstractMetaClass* foobars = classes.findClass("FooBars");
    QCOMPARE(foobars->functions().count(), 4);

    const AbstractMetaClass* lc = templates.first();
    QCOMPARE(lc->functions().count(), 2);
}

void TestTemplates::testTemplateInheritanceMixedWithForwardDeclaration()
{
    const char cppCode[] = "\
    enum SomeEnum { E1, E2 };\
    template<SomeEnum type> struct Future;\
    template<SomeEnum type>\
    struct A {\
        A();\
        void method();\
        friend struct Future<type>;\
    };\
    typedef A<E1> B;\
    template<SomeEnum type> struct Future {};\
    ";
    const char xmlCode[] = "\
    <typesystem package='Package'>\
        <enum-type name='SomeEnum' />\
        <value-type name='A' generate='no' />\
        <value-type name='B' />\
        <value-type name='Future' generate='no' />\
    </typesystem>";

    TestUtil t(cppCode, xmlCode, false);
    AbstractMetaClassList classes = t.builder()->classes();

    AbstractMetaClass* classB = classes.findClass("B");
    QVERIFY(!classB->baseClass());
    QVERIFY(classB->baseClassName().isNull());
    // 3 functions: simple constructor, copy constructor and "method()".
    QCOMPARE(classB->functions().count(), 3);
}

void TestTemplates::testTemplateInheritanceMixedWithNamespaceAndForwardDeclaration()
{
    const char cppCode[] = "\
    namespace Namespace {\
    enum SomeEnum { E1, E2 };\
    template<SomeEnum type> struct Future;\
    template<SomeEnum type>\
    struct A {\
        A();\
        void method();\
        friend struct Future<type>;\
    };\
    typedef A<E1> B;\
    template<SomeEnum type> struct Future {};\
    };\
    ";
    const char xmlCode[] = "\
    <typesystem package='Package'>\
        <namespace-type name='Namespace' />\
        <enum-type name='Namespace::SomeEnum' />\
        <value-type name='Namespace::A' generate='no' />\
        <value-type name='Namespace::B' />\
        <value-type name='Namespace::Future' generate='no' />\
    </typesystem>";

    TestUtil t(cppCode, xmlCode, false);
    AbstractMetaClassList classes = t.builder()->classes();

    AbstractMetaClass* classB = classes.findClass("Namespace::B");
    QVERIFY(!classB->baseClass());
    QVERIFY(classB->baseClassName().isNull());
    // 3 functions: simple constructor, copy constructor and "method()".
    QCOMPARE(classB->functions().count(), 3);
}

QTEST_APPLESS_MAIN(TestTemplates)

#include "testtemplates.moc"

