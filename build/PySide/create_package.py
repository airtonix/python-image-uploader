import sys
import os
import shutil
import subprocess
import optparse
import traceback
import distutils.sysconfig


# Constants
PKG_VERSION = "0.4.2"


# Globals
script_version = "PySide package creator version 0.1"
py_version = "%s.%s" % (sys.version_info[0], sys.version_info[1])
py_include_dir = None
py_library = None
script_dir = None
modules_dir = None
output_dir = None
clean_output = False
download = False
qmake_path = None
qt_version = None
qt_bins_dir = None
qt_plugins_dir = None
modules = [
    ["apiextractor", "master", "git://gitorious.org/pyside/apiextractor.git"],
    ["generatorrunner", "master", "git://gitorious.org/pyside/generatorrunner.git"],
    ["shiboken", "master", "git://gitorious.org/pyside/shiboken.git"],
    ["pyside", "master", "git://gitorious.org/pyside/pyside.git"],
    ["pyside-tools", "master", "git://gitorious.org/pyside/pyside-tools.git"],
]


def run_process(*args):
    shell = False
    if sys.platform == "win32":
        shell = True
    p = subprocess.Popen(args, shell=shell)
    p.communicate()
    return p.returncode


def get_qt_property(prop_name):
    p = subprocess.Popen([qmake_path, "-query", prop_name], shell=False, stdout=subprocess.PIPE)
    prop = p.communicate()[0]
    if p.returncode != 0:
        return None
    return prop.strip()


def replace_in_file(src, dst, vars):
    f = open(src, "rt")
    content =  f.read()
    f.close()
    for k in vars:
        content = content.replace(k, vars[k])
    f = open(dst, "wt")
    f.write(content)
    f.close()


# LINKS:
#   http://snippets.dzone.com/posts/show/6313
def find_executable(executable, path=None):
    """Try to find 'executable' in the directories listed in 'path' (a
    string listing directories separated by 'os.pathsep'; defaults to
    os.environ['PATH']).  Returns the complete filename or None if not
    found
    """
    if path is None:
        path = os.environ['PATH']
    paths = path.split(os.pathsep)
    extlist = ['']
    if os.name == 'os2':
        (base, ext) = os.path.splitext(executable)
        # executable files on OS/2 can have an arbitrary extension, but
        # .exe is automatically appended if no dot is present in the name
        if not ext:
            executable = executable + ".exe"
    elif sys.platform == 'win32':
        pathext = os.environ['PATHEXT'].lower().split(os.pathsep)
        (base, ext) = os.path.splitext(executable)
        if ext.lower() not in pathext:
            extlist = pathext
    for ext in extlist:
        execname = executable + ext
        if os.path.isfile(execname):
            return execname
        else:
            for p in paths:
                f = os.path.join(p, execname)
                if os.path.isfile(f):
                    return f
    else:
        return None


def check_env():
    # Check if the required programs are on system path.
    requiredPrograms = [ "cmake" ];
    if download:
        requiredPrograms.append("git")
    if sys.platform == "win32":
        requiredPrograms.append("nmake")
    else:
        requiredPrograms.append("make")

    for prg in requiredPrograms:
        print "Checking " + prg + "..."
        f = find_executable(prg)
        if not f:
            print "You need the program \"" + prg + "\" on your system path to compile PySide."
            sys.exit(1)
        else:
            print 'Found %s' % f


def get_module(module):
    # Clone sources from git repository
    os.chdir(modules_dir)
    if os.path.exists(module[0]):
        if download:
            print "Deleting folder %s..." % module[0]
            shutil.rmtree(module[0], False)
        else:
            return
    repo = module[2]
    print "Downloading " + module[0] + " sources at " + repo
    if run_process("git", "clone", repo) != 0:
        raise Exception("Error cloning " + repo)


def compile_module(module):
    os.chdir(modules_dir + "/" + module[0])
    if os.path.exists("build") and clean_output:
        print "Deleting build folder..."
        shutil.rmtree("build", False)
    if not os.path.exists("build"):
        os.mkdir("build")
    os.chdir(modules_dir + "/" + module[0] + "/build")

    if modules_dir is None:
        print "Changing to branch " + branch + " in " + module[0]
        branch = module[1]
        if run_process("git", "checkout", branch) != 0:
            raise Exception("Error changing to branch " + branch + " in " + module[0])
    
    if sys.platform == "win32":
        cmake_generator = "NMake Makefiles"
        make_cmd = "nmake"
    else:
        cmake_generator = "Unix Makefiles"
        make_cmd = "make"
    
    print "Configuring " + module[0] + " in " + os.getcwd() + "..."
    args = [
        "cmake",
        "-G", cmake_generator,
        "-DQT_QMAKE_EXECUTABLE=%s" % qmake_path,
        "-DBUILD_TESTS=False",
        "-DPYTHON_EXECUTABLE=%s" % sys.executable,
        "-DPYTHON_INCLUDE_DIR=%s" % py_include_dir,
        "-DPYTHON_LIBRARY=%s" % py_library,
        "-DCMAKE_BUILD_TYPE=Release",
        "-DCMAKE_INSTALL_PREFIX=%s" % output_dir,
        ".."
    ]
    if module[0] == "generatorrunner":
        args.append("-DCMAKE_INSTALL_RPATH_USE_LINK_PATH=yes")
    if run_process(*args) != 0:
        raise Exception("Error configuring " + module[0])
    
    print "Compiling " + module[0] + "..."
    if run_process(make_cmd) != 0:
        raise Exception("Error compiling " + module[0])
    
    print "Testing " + module[0] + "..."
    if run_process("ctest") != 0:
        print "Some " + module[0] + " tests failed!"
    
    print "Installing " + module[0] + "..."
    if run_process(make_cmd, "install/fast") != 0:
        raise Exception("Error pseudo installing " + module[0])


def create_package():
    print "Generating python distribution package..."
    
    os.chdir(script_dir)
    
    pkgsrc_dir = os.path.join(script_dir, "src")
    if os.path.exists(pkgsrc_dir):
        shutil.rmtree(pkgsrc_dir, False)
    os.mkdir(pkgsrc_dir)
    
    # <output>/lib/site-packages/PySide/* -> src/PySide
    src = os.path.join(output_dir, "lib/site-packages/PySide")
    print "Copying PySide sources from %s" % (src)
    shutil.copytree(src, os.path.join(pkgsrc_dir, "PySide"))
    
    # <output>/lib/site-packages/pysideuic/* -> src/pysideuic
    src = os.path.join(output_dir, "lib/site-packages/pysideuic")
    print "Copying pysideuic sources from %s" % (src)
    shutil.copytree(src, os.path.join(pkgsrc_dir, "pysideuic"))
    
    # <output>/bin/pyside-uic -> src/PySide/scripts/uic.py
    src = os.path.join(output_dir, "bin/pyside-uic")
    dst = os.path.join(pkgsrc_dir, "PySide/scripts")
    os.mkdir(dst)
    f = open(os.path.join(dst, "__init__.py"), "wt")
    f.write("# Package")
    f.close()
    dst = os.path.join(dst, "uic.py")
    print "Copying pyside-uic script from %s to %s" % (src, dst)
    shutil.copy(src, dst)
    
    # <output>/bin/pyside.dll -> src/PySide/pyside.dll
    src = os.path.join(output_dir, "bin/pyside.dll")
    print "Copying pyside.dll from %s" % (src)
    shutil.copy(src, os.path.join(pkgsrc_dir, "PySide/pyside.dll"))
    
    # <output>/bin/shiboken.dll -> src/PySide/shiboken.dll
    src = os.path.join(output_dir, "bin/shiboken.dll")
    print "Copying shiboken.dll from %s" % (src)
    shutil.copy(src, os.path.join(pkgsrc_dir, "PySide/shiboken.dll"))
    
    # <qt>/bin/* -> src/PySide
    src = qt_bins_dir
    dst = os.path.join(pkgsrc_dir, "PySide")
    print "Copying Qt binaries from %s" % (src)
    names = os.listdir(qt_bins_dir)
    for name in names:
        if name.endswith(".dll") and not name.endswith("d4.dll"):
            srcname = os.path.join(src, name)
            dstname = os.path.join(dst, name)
            print "Copying \"%s\"" % (srcname)
            shutil.copy(srcname, dstname)
    
    # <qt>/plugins/* -> src/PySide/plugins
    src = qt_plugins_dir
    print "Copying Qt plugins from %s" % (src)
    shutil.copytree(src, os.path.join(pkgsrc_dir, "PySide/plugins"), ignore=shutil.ignore_patterns('*.lib', '*d4.dll'))
    
    # <modules>/examples/* -> src/PySide/examples
    src = os.path.join(modules_dir, "examples")
    if os.path.exists(src):
        print "Copying PySide examples from %s" % (src)
        shutil.copytree(src, os.path.join(pkgsrc_dir, "PySide/examples"))
    
    # Prepare setup.py
    print "Preparing setup.py..."
    version_str = "%sqt%s" % (PKG_VERSION, qt_version.replace(".", "")[0:2]) # Take only major and minor numbers from Qt version
    replace_in_file("setup.py.in", "setup.py", { "${version}": version_str })
    
    # Build package
    print "Building distribution package..."
    if run_process(sys.executable, "setup.py", "bdist_wininst", "--target-version=%s" % py_version) != 0:
        raise Exception("Error building distribution package ")


def main():
    optparser = optparse.OptionParser(usage="create_package [options]", version=script_version)
    optparser.add_option("-e", "--check-environ", dest="check_environ",                         
                         action="store_true", default=False, help="Check the environment")
    optparser.add_option("-q", "--qmake", dest="qmake_path",                         
                         default=None, help="Locate qmake")
    optparser.add_option("-c", "--clean", dest="clean",
                         action="store_true", default=False, help="Clean build output")
    optparser.add_option("-d", "--download", dest="download",
                         action="store_true", default=False, help="Download latest sources from git repository")

    options, args = optparser.parse_args(sys.argv)

    try:
        # Setup globals
        global py_include_dir
        py_include_dir = distutils.sysconfig.get_config_var("INCLUDEPY")
        
        global py_library
        py_prefix = distutils.sysconfig.get_config_var("prefix")
        if sys.platform == "win32":
            py_library = os.path.join(py_prefix, "libs/python%s.lib" % py_version.replace(".", ""))
        else:
            py_library = os.path.join(py_prefix, "lib/libpython%s.so" % py_version)
        if not os.path.exists(py_library):
            print "Failed to locate the Python library %s" % py_library
        
        global script_dir
        script_dir = os.getcwd()
        
        global modules_dir
        modules_dir = os.path.join(script_dir, "modules")
        if not os.path.exists("modules"):
            os.mkdir(modules_dir)
        
        global qmake_path
        installed_qmake_path = find_executable("qmake")
        qmake_path = options.qmake_path or installed_qmake_path
        if not qmake_path or not os.path.exists(qmake_path):
            print "Failed to find qmake. Please specify the path to qmake with --qmake parameter."
            sys.exit(1)
        
        # Add path to this version of Qt to environment if it's not there.
        # Otherwise the "generatorrunner" will not find the Qt libraries
        paths = os.environ['PATH'].lower().split(os.pathsep)
        qt_dir = os.path.dirname(qmake_path)
        if not qt_dir.lower() in paths:
            print "Adding path \"%s\" to environment" % qt_dir
            paths.append(qt_dir)
        os.environ['PATH'] = os.pathsep.join(paths)
        
        global qt_version
        qt_version = get_qt_property("QT_VERSION")
        if not qt_version:
            print "Failed to query the Qt version with qmake %s" % qmake_path
            sys.exit(1)
        
        global qt_bins_dir
        qt_bins_dir = get_qt_property("QT_INSTALL_BINS")
        
        global qt_plugins_dir
        qt_plugins_dir = get_qt_property("QT_INSTALL_PLUGINS")
        
        global clean_output
        clean_output = options.clean
        
        global download
        download = options.download
        
        global output_dir
        output_dir = os.path.join(modules_dir, "output-py%s-qt%s") % (py_version, qt_version)
        
        print "------------------------------------------"
        print "Python executable: %s" % sys.executable
        print "Python includes: %s" % py_include_dir
        print "Python library: %s" % py_library
        print "Script directory: %s" % script_dir
        print "Modules directory: %s" % modules_dir or "<git repository>"
        print "Output directory: %s" % output_dir
        print "Python version: %s" % py_version
        print "qmake path: %s" % qmake_path
        print "Qt version: %s" % qt_version
        print "Qt bins: %s" % qt_bins_dir
        print "Qt plugins: %s" % qt_plugins_dir
        print "------------------------------------------"
        
        # Check environment
        check_env()
        
        if options.check_environ:
            return
        
        if os.path.exists(output_dir) and clean_output:
            print "Deleting output folder..."
            shutil.rmtree(output_dir, False)
        
        # Get and build modules
        for module in modules:
            get_module(module)
            compile_module(module)
        
        # Create python distribution package
        create_package()
    
    except Exception, e:
        print traceback.print_exception(*sys.exc_info())
        sys.exit(1)
    
    sys.exit(0)


if __name__ == "__main__":
    main()
