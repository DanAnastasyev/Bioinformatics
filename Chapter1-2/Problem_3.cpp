#include <fstream>
#include <iostream>
#include <string>
#include <unordered_map>

using namespace std;

bool isAppriximatelyMatch(const string& pattern, const string& line, int pos, int d)
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

auto findApproximateMatchs(const string& pattern, const string& line, int d)
{
	vector<int> approximateMatchPosition;
	for (int i = 0; i < line.length() - pattern.length(); ++i) {
		if (isAppriximatelyMatch(pattern, line, i, d)) {
			approximateMatchPosition.push_back(i);
		}
	}
	return approximateMatchPosition;
}

int main()
{
	ifstream ifs("input.txt", std::ifstream::in);
	ofstream ofs("output.txt", std::ifstream::out);

	string pattern, line;
	int d;
	ifs >> pattern >> line >> d;
	
	for (const auto& matchPos : findApproximateMatchs(pattern, line, d)) {
		ofs << matchPos << " ";
	}

	return 0;
}
