from setuptools_rust import RustExtension, Binding

def get_rust_extensions():
    return [RustExtension("finatic_python.finatic_python", binding=Binding.PyO3)] 