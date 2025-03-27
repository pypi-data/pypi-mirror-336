#!/usr/bin/env python
"""
Command-line interface for the pathik crawler
"""
import argparse
import sys
import os
import json
import subprocess
from . import crawl, crawl_to_r2
from .crawler import get_binary_path

def main():
    """Main entry point for the CLI"""
    parser = argparse.ArgumentParser(description="Pathik - A fast web crawler with Python integration")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Crawl command
    crawl_parser = subparsers.add_parser("crawl", help="Crawl websites and save them locally")
    crawl_parser.add_argument("urls", nargs="+", help="URLs to crawl")
    crawl_parser.add_argument("-o", "--outdir", help="Output directory for crawled files")
    crawl_parser.add_argument("-s", "--sequential", action="store_true", help="Use sequential (non-parallel) crawling")
    
    # R2 crawl command
    r2_parser = subparsers.add_parser("r2", help="Crawl websites and upload to R2")
    r2_parser.add_argument("urls", nargs="+", help="URLs to crawl")
    r2_parser.add_argument("-u", "--uuid", help="UUID to use for file prefixes")
    r2_parser.add_argument("-s", "--sequential", action="store_true", help="Use sequential (non-parallel) crawling")
    
    # Kafka command
    kafka_parser = subparsers.add_parser("kafka", help="Crawl websites and stream to Kafka")
    kafka_parser.add_argument("urls", nargs="+", help="URLs to crawl")
    kafka_parser.add_argument("-s", "--sequential", action="store_true", help="Use sequential (non-parallel) crawling")
    kafka_parser.add_argument("-b", "--brokers", help="Kafka brokers (comma-separated)")
    kafka_parser.add_argument("-t", "--topic", help="Kafka topic to stream to")
    
    # Version command
    version_parser = subparsers.add_parser("version", help="Print version information")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    try:
        if args.command == "crawl":
            result = crawl(
                urls=args.urls, 
                output_dir=args.outdir, 
                parallel=not args.sequential
            )
            
            # Print results summary
            print("\nCrawl Results:")
            print("--------------")
            for url, info in result.items():
                if "error" in info:
                    print(f"❌ {url}: Error - {info['error']}")
                else:
                    print(f"✅ {url}: Success")
                    print(f"   HTML: {info.get('html', 'Not found')}")
                    print(f"   Markdown: {info.get('markdown', 'Not found')}")
            
            # Also write results to a JSON file if output directory is specified
            if args.outdir:
                results_file = os.path.join(args.outdir, "pathik_results.json")
                with open(results_file, "w") as f:
                    json.dump(result, f, indent=2)
                print(f"\nResults saved to: {results_file}")
        
        elif args.command == "r2":
            result = crawl_to_r2(
                urls=args.urls,
                uuid_str=args.uuid,
                parallel=not args.sequential
            )
            
            # Print results summary
            print("\nR2 Upload Results:")
            print("-----------------")
            for url, info in result.items():
                print(f"✅ {url}")
                print(f"   UUID: {info.get('uuid')}")
                print(f"   HTML Key: {info.get('r2_html_key')}")
                print(f"   Markdown Key: {info.get('r2_markdown_key')}")
        
        elif args.command == "kafka":
            # For Kafka we need to use the Go binary directly
            try:
                binary_path = get_binary_path()
                cmd = [binary_path, "-kafka"]
                
                # Add parallel flag if sequential is not specified
                if not args.sequential:
                    cmd.append("-parallel")
                
                # Add Kafka-specific options if provided
                if args.brokers:
                    os.environ["KAFKA_BROKERS"] = args.brokers
                if args.topic:
                    os.environ["KAFKA_TOPIC"] = args.topic
                
                # Add URLs
                cmd.extend(args.urls)
                
                print(f"Running: {' '.join(cmd)}")
                process = subprocess.run(cmd, check=True)
                
                if process.returncode == 0:
                    print("\nKafka Streaming Results:")
                    print("-----------------------")
                    print(f"✅ Successfully streamed {len(args.urls)} URLs to Kafka")
                else:
                    print(f"❌ Error streaming to Kafka, exit code: {process.returncode}")
                    return process.returncode
                    
            except Exception as e:
                print(f"❌ Error executing Kafka command: {e}")
                return 1
        
        elif args.command == "version":
            from . import __version__  # Importing here to avoid circular imports
            print(f"Pathik v{__version__}")
            return 0
        
        return 0
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main()) 