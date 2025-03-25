from setuptools import setup, find_packages

setup(
    name="req-test-align",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "req_test_align": ["templates/*.yml"],
    },
    entry_points={
        "console_scripts": [
            "req-test-align=req_test_align.main:main_entry",
            "rta-metrics=req_test_align.monitor.report_generator:main",
        ],
    },
    install_requires=[
        "openai>=0.27.0",
        "requests>=2.25.0",
        "parso>=0.8.2",
        "javalang>=0.13.0",
        "unidiff>=0.5.5",
        "psutil>=5.9.0",
        "py-cpuinfo>=9.0.0",
        # Add optional GPU monitoring
        "pynvml;platform_system=='Windows' or platform_system=='Linux'",
    ],
    python_requires=">=3.7",
    author="ReqTestAlign",
    description="A tool to align requirements and test cases",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
