# Group Report: Nupe Language NLP Analysis

**Group Name**: Group 01  
**Language**: Nupe  
**Date**: 2024  
**Status**: [In Progress / Completed]

---

## Executive Summary

[Provide a 2-3 sentence overview of your group's work and key findings]

## 1. Data Collection Results

### 1.1 Scraped Data Overview
- **Total Documents**: ___
- **Date Range**: ___ to ___
- **Data Source(s)**: 
  - [List your sources here]

### 1.2 Data Quality
- **Valid JSONL Entries**: ___
- **Failed Scrapes**: ___ (List reasons)
- **Average Text Length**: ___ characters

### 1.3 Challenges & Solutions

[Describe any challenges in data collection and how you addressed them]

---

## 2. Text Processing & Tokenization

### 2.1 Tokenization Statistics
- **Total Tokens**: ___
- **Unique Tokens (Vocabulary)**: ___
- **Type-Token Ratio (TTR)**: ___
- **Average Tokens per Document**: ___

### 2.2 Diacritic Preservation
- **Diacritic Types Preserved**: ẹ, ọ, ṇ, ị, etc.
- **Documents with Diacritics**: ___
- **Coverage**: ___ %

### 2.3 Stop Word Removal
- **Stop Words Removed**: ___
- **Percentage of Total Tokens**: ___ %

### 2.4 Sample Tokenization Results

**Before:**
```
<p>Nupe ọkọ́ diacritics and tone marks.</p>
```

**After:**
```
nupe ọkọ́ diacritics tone marks
```

---

## 3. Zipf's Law Analysis

### 3.1 Frequency Distribution

| Rank | Token | Frequency | Log(Rank) | Log(Frequency) |
|------|-------|-----------|-----------|----------------|
| 1    | ___   | ___       | ___       | ___            |
| 2    | ___   | ___       | ___       | ___            |
| 5    | ___   | ___       | ___       | ___            |
| 10   | ___   | ___       | ___       | ___            |

### 3.2 Zipfian Exponent

**Calculated Exponent (s)**: ___

**Expected Range**: 1.0 - 2.0 (typical for natural languages)

**Interpretation**: 
- If s ≈ 1.0: Strong Zipfian distribution
- If s > 2.0: Distribution is flatter than expected
- If s < 1.0: Distribution is steeper than expected

[Provide your interpretation based on the calculated exponent]

### 3.3 Visualization Notes

[Describe the log-log plot: shape, outliers, goodness of fit, R² value if computed]

### 3.4 Insights

[What does the Zipfian distribution tell us about the Nupe corpus?]

---

## 4. Bigram Language Model

### 4.1 Model Training

- **Corpus Size**: ___ tokens
- **Unigram Coverage**: ___ unique tokens
- **Bigram Types**: ___ unique bigrams
- **Bigram Tokens**: ___ total bigrams

### 4.2 Laplace Smoothing Details

- **Vocabulary Size (V)**: ___
- **Smoothing Parameter**: 1 (Add-1)
- **Coverage of Unseen Bigrams**: Yes / No

### 4.3 Model Evaluation

**Test Set Perplexity**: ___

**Interpretation**:
- Perplexity < 100: Strong model performance
- Perplexity 100-500: Moderate performance
- Perplexity > 500: Model may need refinement

**Your Model Assessment**: ___

### 4.4 Top Bigrams by Probability

| Bigram (w1, w2) | Count | P(w2\|w1) |
|-----------------|-------|-----------|
| (word1, word2)  | ___   | ___       |
| (word3, word4)  | ___   | ___       |
| (word5, word6)  | ___   | ___       |

### 4.5 Model Error Analysis

[Discuss any observed weaknesses or error patterns]

---

## 5. Key Findings & Insights

### 5.1 Linguistic Properties of Nupe (Based on Your Analysis)

[What did you learn about Nupe from this NLP analysis?]

### 5.2 Challenges Encountered

1. **Challenge 1**: [Description and Solution]
2. **Challenge 2**: [Description and Solution]
3. **Challenge 3**: [Description and Solution]

### 5.3 Lessons Learned

[What NLP concepts did this assignment reinforce or introduce?]

---

## 6. Comparison with Expected Baselines

| Metric | Your Result | Typical Range | Status |
|--------|-------------|----------------|--------|
| Zipfian Exponent | ___ | 1.0-2.0 | ✓ / ✗ |
| Model Perplexity | ___ | <500 (ideal) | ✓ / ✗ |
| Diacritic Coverage | ___ % | >95% | ✓ / ✗ |

---

## 7. Recommendations for Future Work

1. [Suggestion 1]: ...
2. [Suggestion 2]: ...
3. [Suggestion 3]: ...

---

## 8. Code Quality & Documentation

- **Code Reusability**: [Your assessment]
- **Documentation**: [Your assessment]
- **Testing**: [Your assessment]
- **Reproducibility**: [Your assessment]

---

## Appendix: References

1. Jurafsky, D., & Martin, J. H. (2020). *Speech and Language Processing* (3rd ed.). https://web.stanford.edu/~jurafsky/slp3/
2. Zipf, G. K. (1949). *Human Behavior and the Principle of Least Effort*.
3. [Add Nupe language resources]
4. [Add other relevant citations]

---

## Appendix: Git Commit Log

```
$ git log --oneline
[Include last 10 commits here]
```

**Contributors**: [List all group members and their contributions]

---

**Report Submitted**: [Date]  
**All Parts Complete**: Yes / No  
**Ready for Submission**: Yes / No
