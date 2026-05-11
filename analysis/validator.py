"""
Validation and startup checks for analysis components
"""

import logging
import sys
from typing import Dict, List, Optional

class AnalysisValidator:
    """Validator for analysis components and dependencies"""
    
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.successes = []
    
    def validate_dependencies(self) -> Dict:
        """Validate all required dependencies"""
        logging.info("Starting dependency validation")
        
        # Check core required modules (that don't need compilation)
        required_modules = {
            'requests': 'HTTP requests library',
            'bs4': 'BeautifulSoup4 for web scraping',
        }
        
        # Check optional modules (that may need compilation)
        optional_modules = {
            'streamlit': 'Streamlit UI framework',
            'pandas': 'Data manipulation library',
            'lxml': 'Fast XML/HTML parser (optional)',
        }
        
        for module, description in required_modules.items():
            try:
                if module == 'bs4':
                    import bs4
                    self.successes.append(f"[OK] {description} (v{bs4.__version__})")
                elif module == 'requests':
                    import requests
                    self.successes.append(f"[OK] {description} (v{requests.__version__})")
            except ImportError as e:
                self.errors.append(f"[ERROR] {description} - Missing: {e}")
        
        for module, description in optional_modules.items():
            try:
                if module == 'streamlit':
                    import streamlit
                    self.successes.append(f"[OK] {description} (v{streamlit.__version__})")
                elif module == 'pandas':
                    import pandas
                    self.successes.append(f"[OK] {description} (v{pandas.__version__})")
                elif module == 'lxml':
                    import lxml
                    self.successes.append(f"[OK] {description} (v{lxml.__version__})")
            except ImportError:
                if module in ['streamlit', 'pandas']:
                    self.warnings.append(f"[WARN] {description} - Not installed (UI may not work)")
                else:
                    self.warnings.append(f"[WARN] {description} - Not installed (using fallback)")
        
        return {
            'errors': self.errors,
            'warnings': self.warnings,
            'successes': self.successes,
            'valid': len(self.errors) == 0
        }
    
    def validate_analysis_functions(self) -> Dict:
        """Validate analysis functions are available"""
        logging.info("Validating analysis functions")
        
        try:
            # Test rule-based analysis
            from .rule_engine import RuleBasedAnalyzer, rule_analyzer
            self.successes.append("[OK] Rule-based analysis engine loaded")
            
            # Test scraper
            from .scraper import JobScraper, job_scraper
            self.successes.append("[OK] Job scraper engine loaded")
            
            # Test backward compatibility functions
            from .rule_engine import _rule_based_analysis
            from .scraper import is_valid_job_url, _fetch_job_page, _extract_title_from_url, _extract_domain
            self.successes.append("[OK] Backward compatibility functions available")
            
        except ImportError as e:
            self.errors.append(f"[ERROR] Analysis functions not available: {e}")
        
        return {
            'errors': self.errors,
            'warnings': self.warnings,
            'successes': self.successes,
            'valid': len(self.errors) == 0
        }
    
    def validate_utils_imports(self) -> Dict:
        """Validate utils module imports"""
        logging.info("Validating utils module imports")
        
        try:
            # Try importing core utils functions without streamlit
            import sys
            import os
            sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            
            # Test core analysis functions directly
            from analysis.rule_engine import _rule_based_analysis
            from analysis.scraper import is_valid_job_url, _fetch_job_page
            self.successes.append("[OK] Core analysis functions imported")
            
            # Check if streamlit is available for UI functions
            try:
                import streamlit
                from utils import bi, simulate_analysis, is_valid_email, is_valid_phone, _show_result
                self.successes.append("[OK] All utils functions imported successfully")
            except ImportError:
                self.warnings.append("[WARN] Streamlit not available - UI functions will not work")
                # Still validate core analysis works
                self.successes.append("[OK] Core analysis functionality available")
            
        except Exception as e:
            self.errors.append(f"[ERROR] Core analysis import failed: {e}")
        
        return {
            'errors': self.errors,
            'warnings': self.warnings,
            'successes': self.successes,
            'valid': len(self.errors) == 0
        }
    
    def run_full_validation(self) -> Dict:
        """Run complete validation suite"""
        logging.info("Running full validation suite")
        
        # Reset status
        self.errors = []
        self.warnings = []
        self.successes = []
        
        # Run all validations
        dep_result = self.validate_dependencies()
        func_result = self.validate_analysis_functions()
        utils_result = self.validate_utils_imports()
        
        # Combine results
        all_errors = self.errors
        all_warnings = self.warnings
        all_successes = self.successes
        
        is_valid = len(all_errors) == 0
        
        # Log results
        if is_valid:
            logging.info("All validations passed")
        else:
            logging.error(f"Validation failed with {len(all_errors)} errors")
        
        return {
            'valid': is_valid,
            'errors': all_errors,
            'warnings': all_warnings,
            'successes': all_successes,
            'dependency_result': dep_result,
            'function_result': func_result,
            'utils_result': utils_result
        }
    
    def print_validation_report(self, result: Dict):
        """Print validation report to console"""
        print("\n" + "="*60)
        print("SNIFFJOB ANALYSIS VALIDATION REPORT")
        print("="*60)
        
        if result['valid']:
            print("STATUS: ALL VALIDATIONS PASSED")
        else:
            print("STATUS: VALIDATION FAILED")
        
        if result['successes']:
            print("\nSUCCESSFUL:")
            for success in result['successes']:
                print(f"  {success}")
        
        if result['warnings']:
            print("\nWARNINGS:")
            for warning in result['warnings']:
                print(f"  {warning}")
        
        if result['errors']:
            print("\nERRORS:")
            for error in result['errors']:
                print(f"  {error}")
        
        print("="*60)

# Global validator instance
validator = AnalysisValidator()

def validate_startup():
    """Run startup validation and exit if critical errors found"""
    result = validator.run_full_validation()
    
    if not result['valid']:
        validator.print_validation_report(result)
        print("\nCRITICAL: Cannot start application due to missing dependencies")
        print("Please install missing packages and restart the application.")
        sys.exit(1)
    else:
        logging.info("Startup validation passed")
        return True
