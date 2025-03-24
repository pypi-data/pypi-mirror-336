import jpype

def test_jpype_start():
    if not jpype.isJVMStarted():
        jpype.startJVM()  # Start the JVM (only one allowed per process)
    else:
        print("JVM already started")
    # Simple call to verify the JVM is working.
    java_lang_System = jpype.JPackage("java.lang").System
    version = java_lang_System.getProperty("java.version")
    assert version is not None

def test_dummy():
    # A dummy test to force multiple tests in one run.
    assert True