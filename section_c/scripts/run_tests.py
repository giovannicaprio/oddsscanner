#!/usr/bin/env python3
import sys
import pytest
import coverage

def run_tests_with_coverage():
    """Run tests with coverage reporting."""
    # Start coverage measurement
    cov = coverage.Coverage(
        source=['src'],
        omit=['*/__init__.py', 'tests/*'],
    )
    cov.start()

    # Run pytest
    exit_code = pytest.main(['tests/', '-v'])

    # Stop coverage measurement
    cov.stop()
    cov.save()

    # Generate reports
    print('\nCoverage Summary:')
    cov.report()
    
    # Generate HTML report
    cov.html_report(directory='coverage_html')
    
    print('\nDetailed coverage report generated in coverage_html/index.html')
    
    return exit_code

if __name__ == '__main__':
    sys.exit(run_tests_with_coverage()) 