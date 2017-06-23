#include <fstream>
#include <iostream>
#include <string>
#include <unordered_map>
#include <algorithm>
#include <iterator>
#include <random>

using namespace std;

auto calcHammingDistance(const string& text, int startIndex, int k, const string& pattern)
{
	auto distance = 0;
	for (int i = 0; i < k; ++i) {
		distance += int(text[i + startIndex] != pattern[i]);
	}
	return distance;
}

auto distanceBetweenPatternAndStrings(const string& pattern, const vector<string>& dna)
{
	auto k = pattern.length();
	auto distance = 0;
	for (const auto& text : dna) {
		int hammingDistance = k + 1;
		for (int i = 0; i < text.length() - k + 1; ++i) {
			hammingDistance = min(hammingDistance, calcHammingDistance(text, i, k, pattern));
		}
		distance += hammingDistance;
	}
	return distance;
}

int main()
{
	ifstream ifs("input.txt", ifstream::in);

	string pattern;
	ifs >> pattern;
	vector<string> dna;
	copy(istream_iterator<string>(ifs), {}, back_inserter(dna));

	cout << distanceBetweenPatternAndStrings(pattern, dna) << endl;

	return 0;
}
