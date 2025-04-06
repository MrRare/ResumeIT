#!/usr/bin/env python
"""
Script to index all resumes in the data/resumes directory
"""
from resume_processor import process_all_resumes

if __name__ == "__main__":
    print("Starting resume indexing...")
    process_all_resumes()
    print("Indexing complete!")