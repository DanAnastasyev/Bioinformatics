#include <fstream>
#include <iostream>
#include <string>
#include <unordered_map>
#include <algorithm>
#include <iterator>
#include <random>

using namespace std;

auto generateMotifs(const vector<string>& dna, int k)
{
	static default_random_engine generator;
	static uniform_int_distribution<int> distribution(0, dna[0].length() - k + 1);

	vector<string> bestMotifs;
	for_each(dna.begin(), dna.end(),
		[&bestMotifs, k](const string& line) {
			bestMotifs.push_back(line.substr(distribution(generator), k));
		}
	);
	return bestMotifs;
}

auto buildProfile(const vector<string>& motifs, int k)
{
	static const vector<char> nucleotides = { 'A', 'C', 'G', 'T' };
	unordered_map<char, vector<double>> profile;
	for (auto nucleotide : nucleotides) {
		profile[nucleotide] = vector<double>(k, .0);
		for (int j = 0; j < k; ++j) {
			int count = count_if(motifs.begin(), motifs.end(),
				[nucleotide, j](const string& motif) { return motif[j] == nucleotide; });
			profile[nucleotide][j] = static_cast<double>(count + 1) / (motifs.size() + nucleotides.size());
		}
	}
	return profile;
}

auto getKMerScore(const string& line, int start, int k, 
	const unordered_map<char, vector<double>>& profile)
{
	double res = 1.0;
	for (int i = 0; i < k; ++i) {
		res *= profile.at(line[start + i])[i];
	}
	return res;
}

auto getProfileMostProbable(const string& line, int k,
	const unordered_map<char, vector<double>>& profile)
{
	auto bestKMerPos = 0;
	auto bestKMerScore = 0.0;
	for (int i = 0; i < line.length() - k + 1; ++i) {
		auto score = getKMerScore(line, i, k, profile);
		if (score > bestKMerScore) {
			bestKMerPos = i;
			bestKMerScore = score;
		}
	}
	return line.substr(bestKMerPos, k);
}

char getMostFreqInColumn(const vector<string>& motifs, int column)
{
	unordered_map<char, int> counts = {
		{'A', 0}, {'C', 0}, {'G', 0}, {'T', 0}
	};
	
	for (int i = 0; i < motifs.size(); ++i) {
		++counts[motifs[i][column]];
	}
	return max_element(counts.begin(), counts.end(), 
		[](auto&& lhs, auto&& rhs) { return lhs.second < rhs.second; })->first;
}

auto getMotifsScore(const vector<string>& motifs, int k)
{
	auto score = 0;
	for (auto i = 0; i < k; ++i) {
		auto mostFreqNucl = getMostFreqInColumn(motifs, i);
		score += count_if(motifs.begin(), motifs.end(), 
			[i, mostFreqNucl](auto&& motif) { return motif[i] != mostFreqNucl; });
	}
	return score;
}

auto buildMotifs(const vector<string>& dna,
	const unordered_map<char, vector<double>>& profile, int k)
{
	vector<string> motifs;
	for_each(dna.begin(), dna.end(),
		[&motifs, &profile, k](const string& line) {
			motifs.push_back(getProfileMostProbable(line, k, profile));
		}
	);
	return motifs;
}

auto randomizedMotifSearch(const vector<string>& dna, int k)
{
	auto motifs = generateMotifs(dna, k);
	auto bestMotifs = motifs;
	auto bestMotifsScore = getMotifsScore(motifs, k);
	while (true) {
		motifs = buildMotifs(dna, buildProfile(motifs, k), k);
		auto score = getMotifsScore(motifs, k);
		if (score < bestMotifsScore) {
			bestMotifsScore = score;
			bestMotifs = motifs;
		} else {
			return motifs;
		}
	}
}

auto bestRandomizedMotifSearch(const vector<string>& dna, int k, int launchCount)
{
	auto bestMotifs = generateMotifs(dna, k);
	auto bestMotifsScore = getMotifsScore(bestMotifs, k);
	for (int i = 0; i < launchCount; ++i) {
		auto newMotifs = randomizedMotifSearch(dna, k);
		auto newMotifsScore = getMotifsScore(newMotifs, k);
		if (newMotifsScore < bestMotifsScore) {
			bestMotifsScore = newMotifsScore;
			bestMotifs = newMotifs;
		}
	}
	return bestMotifs;
}

int main()
{
	ifstream ifs("input.txt", ifstream::in);

	int k, t;
	ifs >> k >> t;
	vector<string> dna;
	copy(istream_iterator<string>(ifs), {}, back_inserter(dna));

	for (const auto& motif : bestRandomizedMotifSearch(dna, k, 1000)) {
		cout << motif << endl;
	}

	return 0;
}

