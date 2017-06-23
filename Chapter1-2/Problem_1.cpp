#include <fstream>
#include <iostream>
#include <string>
#include <unordered_set>
#include <unordered_map>

using namespace std;

bool isClump( const vector<int>& kmerPositions, int newPosition, int L, int t )
{
	if (kmerPositions.size() + 1 < t) {
		return false;
	}
	int numberOfAppearences = 0;
	for( auto position : kmerPositions ) {
		if (newPosition - position < L) {
			++numberOfAppearences;
		}
	}
	return numberOfAppearences + 1 >= t;
}

unordered_set<string> findClumps(const string& line, int k, int L, int t)
{
	unordered_map<string, vector<int>> kmersPositions;
	unordered_set<string> foundKmers;
	for (int i = 0; i < line.length() - k; ++i) {
		auto kmer = line.substr(i, k);
		if (foundKmers.find(kmer) != foundKmers.end()) {
			continue;
		}
		if (isClump(kmersPositions[kmer], i, L, t)) {
			foundKmers.insert(kmer);
		} else {
			kmersPositions[kmer].push_back(i);
		}
	}
	return foundKmers;
}

int main()
{
	ifstream ifs("input.txt", std::ifstream::in);

	string line;
	ifs >> line;

	int k, L, t;
	ifs >> k >> L >> t;

	for (const auto& clump : findClumps(line, k, L, t)) {
		cout << clump << " ";
	}

	return 0;
}
