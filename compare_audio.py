import argparse
from audio_analyzer import analyze_audio
import json

def main():
    parser = argparse.ArgumentParser(description="Compare audio analysis of two files.")
    parser.add_argument("file1", help="First audio file")
    parser.add_argument("file2", help="Second audio file")
    args = parser.parse_args()

    print(f"Analyzing {args.file1}...")
    res1 = analyze_audio(args.file1)
    
    print(f"Analyzing {args.file2}...")
    res2 = analyze_audio(args.file2)

    print("\nComparison:")
    print(f"{'Feature':<30} | {'File 1':<20} | {'File 2':<20}")
    print("-" * 76)
    
    all_keys = set(res1.keys()) | set(res2.keys())
    for key in sorted(all_keys):
        val1 = res1.get(key, "N/A")
        val2 = res2.get(key, "N/A")
        print(f"{key:<30} | {str(val1):<20} | {str(val2):<20}")

if __name__ == "__main__":
    main()
