# File location: tests/autograder_eval.py

import pytest
import json
import subprocess
import sys
from pathlib import Path

class TestJSONLSchema:
    """Validate raw JSONL data files."""
    
    def test_raw_jsonl_schema(self):
        data_dir = Path("data")
        assert data_dir.exists(), "data/ directory not found"
        
        jsonl_files = list(data_dir.glob("*/raw/*.jsonl"))
        assert len(jsonl_files) > 0, "No .jsonl files found in data/*/raw/"
        
        for jsonl_file in jsonl_files:
            with open(jsonl_file, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    if not line:
                        continue
                    
                    try:
                        entry = json.loads(line)
                    except json.JSONDecodeError as e:
                        pytest.fail(f"Invalid JSON at {jsonl_file}:{line_num}: {e}")
                    
                    required_keys = {'id', 'url', 'date_retrieved', 'raw_text'}
                    missing_keys = required_keys - set(entry.keys())
                    assert not missing_keys, f"Missing keys in {jsonl_file}:{line_num}: {missing_keys}"
                    
                    assert isinstance(entry['id'], int), f"'id' must be int in {jsonl_file}"
                    assert isinstance(entry['url'], str), f"'url' must be str in {jsonl_file}"
                    assert isinstance(entry['date_retrieved'], str), f"'date_retrieved' must be str in {jsonl_file}"
                    assert isinstance(entry['raw_text'], str), f"'raw_text' must be str in {jsonl_file}"

class TestProcessedCorpus:
    """Validate processed tokenized text files."""
    
    def test_processed_corpus_format(self):
        data_dir = Path("data")
        txt_files = list(data_dir.glob("*/processed/*.txt"))
        assert len(txt_files) > 0, "No .txt files found in data/*/processed/"
        
        for txt_file in txt_files:
            with open(txt_file, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    line_stripped = line.rstrip('\n')
                    if not line_stripped:
                        continue
                    
                    tokens = line_stripped.split(' ')
                    assert all(token for token in tokens), f"Multiple spaces found in {txt_file}:{line_num}"
                    assert not line_stripped.startswith(' '), f"Line starts with space in {txt_file}:{line_num}"
                    assert not line_stripped.endswith(' '), f"Line ends with space in {txt_file}:{line_num}"
                    assert '\t' not in line_stripped, f"Tab character found in {txt_file}:{line_num}"
                    assert '\r' not in line_stripped, f"Carriage return found in {txt_file}:{line_num}"

class TestBigramModel:
    """Test the BigramModel implementation dynamically per PR."""
    
    def test_bigram_perplexity(self):
        # 1. Identify modified/added files in this specific Pull Request
        try:
            result = subprocess.run(
                ['git', 'diff', '--name-only', 'HEAD^1', 'HEAD'],
                capture_output=True, text=True, check=True
            )
            changed_files = result.stdout.strip().split('\n')
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Could not read Git history. Error: {e}")

        # 2. Extract the submitting student group folder
        student_dir = None
        for file_path in changed_files:
            if file_path.startswith("submissions/") and "HW1_assignment" in file_path:
                student_dir = Path(file_path).parent
                break
                
        if not student_dir:
            pytest.fail("Could not find any modified 'HW1_assignment' files in this PR. Did you commit and push your work?")

        # 3. Locate converted Python module
        py_file_path = student_dir / "HW1_assignment.py"
        if not py_file_path.exists():
            pytest.fail(f"Could not find HW1_assignment.py in {student_dir}. Ensure your notebook is named correctly.")

        # 4. Extract language name from directory convention (e.g., 'group_01_nupe' -> 'nupe')
        language = student_dir.name.split('_')[-1]
        
        corpus_path = Path(f"data/{language}/processed/{language}_corpus.txt")
        test_path = Path(f"tests/test_{language}_unseen.txt")
        
        assert corpus_path.exists(), f"Expected training corpus not found at {corpus_path}"
        assert test_path.exists(), f"Expected test evaluation file not found at {test_path}"

        # 5. Dynamically load student assignment module
        sys.path.insert(0, str(student_dir))
        
        try:
            from HW1_assignment import BigramModel
        except ImportError as e:
            pytest.fail(f"Could not import BigramModel from {student_dir}. Error: {e}")
        
        # 6. Execute model evaluation
        model = BigramModel()
        bigram_count = model.fit(str(corpus_path))
        
        assert bigram_count > 0, "Model fit returned no bigrams"
        assert model.vocab_size > 0, "Model vocabulary is empty"
        
        perplexity = model.compute_perplexity(str(test_path))
        
        assert isinstance(perplexity, (int, float)), f"Perplexity must be numeric, got {type(perplexity).__name__}"
        assert perplexity > 0, f"Perplexity must be positive, got {perplexity}"
        assert perplexity < float('inf'), "Perplexity is infinite"
        assert perplexity < 1000, f"Perplexity {perplexity:.2f} is too high (should be < 1000)"

class TestGitCollaboration:
    """Verify multi-author collaboration via git commit logs."""
    
    def test_git_commit_count(self):
        try:
            # -sne prints summary sorted by commit count with email addresses included
            # HEAD^1..HEAD ensures we ONLY evaluate commits introduced in this Pull Request
            result = subprocess.run(
                ['git', 'shortlog', '-sne', 'HEAD^1..HEAD'],
                capture_output=True, text=True, check=True, timeout=10
            )
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError) as e:
            pytest.skip(f"Could not run git shortlog: {e}")
        
        output = result.stdout.strip()
        assert output, "No commits found in this PR range (verify fetch-depth: 0 in your workflow YAML)."
        
        # Filter for distinct committer entries (Name <email>)
        authors = [line for line in output.split('\n') if line.strip()]
        author_count = len(authors)
        
        assert author_count >= 2, \
            f"Expected at least 2 unique author emails in this PR, found {author_count}.\n" \
            f"All group members must commit code individually.\n" \
            f"PR Committers recorded:\n{output}"

if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])