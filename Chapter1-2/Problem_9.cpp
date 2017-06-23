#include <fstream>
#include <iostream>
#include <string>
#include <unordered_map>
#include <algorithm>
#include <iterator>
#include <random>

using namespace std;

static default_random_engine generator;

auto generateMotifs(const vector<string>& dna, int k)
{
	static uniform_int_distribution<int> distribution(0, dna[0].length() - k);

	vector<string> bestMotifs;
	for_each(dna.begin(), dna.end(),
		[&bestMotifs, k](const string& line) {
			bestMotifs.push_back(line.substr(distribution(generator), k));
		}
	);
	return bestMotifs;
}

auto buildProfile(const vector<string>& motifs, int k, int excludedMotifIndex = -1)
{
	static const vector<char> nucleotides = { 'A', 'C', 'G', 'T' };
	unordered_map<char, vector<double>> profile;
	for (auto nucleotide : nucleotides) {
		profile[nucleotide] = vector<double>(k, .0);
		for (int j = 0; j < k; ++j) {
			int count = 0;
			for (int i = 0; i < motifs.size(); ++i) {
				count += int(i != excludedMotifIndex && motifs[i][j] == nucleotide);
			}
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

auto generateKMerByProfile(const string& line, 
	const unordered_map<char, vector<double>>& profile, int k)
{
	vector<double> kMersWeights;
	for (int i = 0; i < line.size() - k + 1; ++i) {
		kMersWeights.push_back(getKMerScore(line, i, k, profile));
	}
	discrete_distribution<int> kMersDistribution(kMersWeights.begin(), kMersWeights.end());
	return line.substr(kMersDistribution(generator), k);
}

auto gibbsSampler(const vector<string>& dna, int k, int N)
{
	static uniform_int_distribution<int> distribution(0, dna.size() - 1);

	auto motifs = generateMotifs(dna, k);
	auto bestMotifs = motifs;
	auto bestMotifsScore = getMotifsScore(motifs, k);
	for (int i = 0; i < N; ++i) {
		int excludedIndex = distribution(generator);
		auto profile = buildProfile(motifs, k, excludedIndex);
		motifs[excludedIndex] = generateKMerByProfile(dna[excludedIndex], profile, k);

		auto score = getMotifsScore(motifs, k);
		if (score < bestMotifsScore) {
			bestMotifsScore = score;
			bestMotifs = motifs;
		}
	}
	return bestMotifs;
}

auto bestRandomizedMotifSearch(const vector<string>& dna, int k, int N, int launchCount)
{
	auto bestMotifs = generateMotifs(dna, k);
	auto bestMotifsScore = getMotifsScore(bestMotifs, k);
	for (int i = 0; i < launchCount; ++i) {
		auto newMotifs = gibbsSampler(dna, k, N);
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

	int k, t, N;
	ifs >> k >> t >> N;
	vector<string> dna;
	copy(istream_iterator<string>(ifs), {}, back_inserter(dna));

	for (const auto& motif : bestRandomizedMotifSearch(dna, k, N, 20)) {
		cout << motif << endl;
	}

	return 0;
}

