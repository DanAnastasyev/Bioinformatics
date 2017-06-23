#include <fstream>
#include <iostream>
#include <string>
#include <unordered_map>
#include <algorithm>

using namespace std;

bool isApproximatelyMatch(const string& pattern, const string& line, int pos, int d)
{
	int hammingDistance = 0;
	for (int i = 0; i < pattern.length(); ++i) {
		if (line[i + pos] != pattern[i]) {
			++hammingDistance;
			if (hammingDistance > d) {
				return false;
			}
		}
	}
	return true;
}

const unordered_map<char, char> substitutions { 
	{ 'A', 'T' }, 
	{ 'T', 'A' },
	{ 'C', 'G' },
	{ 'G', 'C' }
};

bool isReverseComplementApproximatelyMatch(const string& pattern, 
	const string& line, int pos, int d)
{
	int hammingDistance = 0;
	int patternLength = pattern.length();
	for (int i = 0; i < patternLength; ++i) {
		if (line[i + pos] != substitutions.at(pattern[patternLength - i - 1])) {
			++hammingDistance;
			if (hammingDistance > d) {
				return false;
			}
		}
	}
	return true;
}

const string Alphabet = "ACGT";

auto generateNextPattern(int k, const string& pattern, string& newPattern)
{
	newPattern = pattern;
	for (int i = k - 1; i >= 0; --i) {
		if (pattern[i] != Alphabet.back()) {
			newPattern[i] = Alphabet[Alphabet.find(pattern[i]) + 1];
			return true;
		} else {
			newPattern[i] = Alphabet.front();
		}
	}
	return false;
}

auto generatePatterns(int k)
{
	vector<pair<string, int>> possiblePatterns{ make_pair(string(k, 'A'), 0) };
	string pattern;
	while (generateNextPattern(k, possiblePatterns.back().first, pattern)) {
		possiblePatterns.push_back(make_pair(pattern, 0));
	}
	return possiblePatterns;
}

auto getMostFrequentPatterns(const vector<pair<string, int>>& patterns)
{
	auto max = max_element(patterns.begin(), patterns.end(),
		[](const pair<string, int>& first, const pair<string, int>& second) {
		return first.second < second.second;
	});

	auto topFreq = max->second;
	vector<string> mostFrequentPatterns;
	for (int i = 0; i < patterns.size(); ++i) {
		if (patterns[i].second == topFreq) {
			mostFrequentPatterns.push_back(patterns[i].first);
		}
	}
	return mostFrequentPatterns;
}

auto findMostFrequentPatterns(const string& line, int k, int d)
{
	auto patterns = generatePatterns(k);
	for (int i = 0; i <= line.length() - k; ++i) {
		for (auto& patternToFreq : patterns) {
			if (isApproximatelyMatch(patternToFreq.first, line, i, d)) {
				++patternToFreq.second;
			}
			if (isReverseComplementApproximatelyMatch(patternToFreq.first, line, i, d)) {
				++patternToFreq.second;
			}
		}
	}
	return getMostFrequentPatterns(patterns);
}

int main()
{
	ifstream ifs("input.txt", ifstream::in);

	string line;
	int k, d;
	ifs >> line >> k >> d;

	for (const auto& pattern : findMostFrequentPatterns(line, k, d)) {
		cout << pattern << " ";
	}

	return 0;
}
