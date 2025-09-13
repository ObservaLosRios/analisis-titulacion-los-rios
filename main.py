"""Main ETL execution script.

This script provides the entry point for executing the ETL pipeline
with command-line interface and comprehensive error handling.
"""

import argparse
import sys
from pathlib import Path
from typing import Optional

# Add src to Python path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.etl_pipeline import ETLPipeline
from src.data_pipeline import ETLError
from src.config import get_settings, get_path_config


def create_argument_parser() -> argparse.ArgumentParser:
    """Create command-line argument parser.
    
    Returns:
        Configured ArgumentParser instance
    """
    parser = argparse.ArgumentParser(
        description="ETL Pipeline for Análisis de Titulación - Región de Los Ríos",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                          # Run full pipeline
  python main.py --extract-only           # Run extraction only
  python main.py --validate-only          # Run validation only
  python main.py --regional-summary       # Show regional summary
  python main.py --output custom_file.csv # Custom output filename
  python main.py --quality-threshold 85   # Set quality threshold to 85%
        """
    )
    
    # Pipeline execution modes
    mode_group = parser.add_mutually_exclusive_group()
    mode_group.add_argument(
        "--extract-only",
        action="store_true",
        help="Run only data extraction step"
    )
    mode_group.add_argument(
        "--validate-only",
        action="store_true",
        help="Run only data validation step"
    )
    mode_group.add_argument(
        "--regional-summary",
        action="store_true",
        help="Generate regional data summary"
    )
    
    # Pipeline configuration
    parser.add_argument(
        "--output",
        type=str,
        help="Output filename for cleaned data (default: auto-generated)"
    )
    parser.add_argument(
        "--quality-threshold",
        type=float,
        default=75.0,
        help="Minimum data quality threshold (0-100, default: 75.0)"
    )
    parser.add_argument(
        "--data-source",
        type=str,
        help="Custom data source file path (for validation-only mode)"
    )
    
    # Logging and debugging
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug mode with detailed error information"
    )
    
    return parser


def print_banner():
    """Print application banner."""
    banner = """
╔══════════════════════════════════════════════════════════════════╗
║                    ETL Pipeline - Los Ríos                      ║
║              Análisis de Titulación Universitaria               ║
║                                                                  ║
║  Universidad Austral de Chile - Región de Los Ríos             ║
║  Implementado con principios SOLID y Clean Code                 ║
╚══════════════════════════════════════════════════════════════════╝
"""
    print(banner)


def main():
    """Main execution function."""
    # Parse command-line arguments
    parser = create_argument_parser()
    args = parser.parse_args()
    
    # Print banner
    print_banner()
    
    try:
        # Initialize configuration
        settings = get_settings()
        path_config = get_path_config()
        
        print(f"🎯 Target Region: {settings.target_region}")
        print(f"📁 Data Path: {path_config.raw_data_path}")
        print(f"📊 Quality Threshold: {args.quality_threshold}%")
        print("=" * 70)
        
        # Initialize ETL pipeline
        pipeline = ETLPipeline(quality_threshold=args.quality_threshold)
        
        # Execute based on mode
        if args.extract_only:
            print("🔄 Running extraction only...")
            result = pipeline.run_extraction_only()
            print(f"✅ Extraction completed: {result.records_processed:,} records extracted")
            
        elif args.validate_only:
            print("🔍 Running validation only...")
            quality_report = pipeline.run_validation_only(args.data_source)
            
            print(f"📋 Validation Results:")
            print(f"   Total Records: {quality_report.total_records:,}")
            print(f"   Valid Records: {quality_report.valid_records:,}")
            print(f"   Quality Score: {quality_report.data_quality_score:.1f}%")
            
            if quality_report.validation_errors:
                print(f"   Validation Errors: {len(quality_report.validation_errors)}")
                if args.verbose:
                    for error in quality_report.validation_errors[:5]:
                        print(f"     - {error}")
            
        elif args.regional_summary:
            print("🗺️  Generating regional summary...")
            summary = pipeline.get_regional_summary()
            
            if "error" in summary:
                print(f"❌ Error: {summary['error']}")
                return 1
            
            print(f"📊 Regional Data Summary:")
            print(f"   Total Records: {summary.get('total_records', 0):,}")
            print(f"   Target Region ({summary.get('target_region', 'Unknown')}): "
                  f"{summary.get('target_region_records', 0):,} records "
                  f"({summary.get('target_region_percentage', 0):.1f}%)")
            
            if args.verbose and 'counts_by_region' in summary:
                print("\n   Records by Region:")
                for region, count in sorted(summary['counts_by_region'].items())[:10]:
                    print(f"     - {region}: {count:,}")
            
        else:
            # Run full pipeline
            print("🚀 Running full ETL pipeline...")
            result = pipeline.run_full_pipeline(args.output)
            
            print(f"\n🎉 Pipeline completed successfully!")
            print(f"   Records Processed: {result.records_processed:,}")
            print(f"   Execution Time: {result.execution_time_seconds:.2f} seconds")
            print(f"   Output File: {result.output_file_path}")
            
            if result.quality_report:
                print(f"   Data Quality Score: {result.quality_report.data_quality_score:.1f}%")
                
                if result.quality_report.data_quality_score < args.quality_threshold:
                    print(f"   ⚠️  Warning: Quality below threshold ({args.quality_threshold}%)")
        
        print("\n✅ Process completed successfully!")
        return 0
        
    except ETLError as e:
        print(f"\n❌ ETL Pipeline Error: {e.message}")
        if args.debug and e.original_error:
            print(f"   Original Error: {e.original_error}")
            import traceback
            traceback.print_exc()
        return 1
        
    except KeyboardInterrupt:
        print(f"\n⏹️  Process interrupted by user")
        return 1
        
    except Exception as e:
        print(f"\n❌ Unexpected Error: {str(e)}")
        if args.debug:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
