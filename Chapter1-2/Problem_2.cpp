#include <fstream>
#include <iostream>
#include <string>
#include <vector>

using namespace std;

auto findSkewPositions(const string& path)
{
	int skewCounter = 0;
	int minSkew = skewCounter;
	vector<int> minSkewPositions;

	ifstream ifs(path, std::ifstream::in);

	char symbol;
	int i = 0;
	while (ifs.get(symbol)) {
		skewCounter += symbol == 'G' ? 1 : (symbol == 'C' ? -1 : 0);
		if (skewCounter < minSkew) {
			minSkew = skewCounter;
			minSkewPositions.clear();
			minSkewPositions.push_back(i);
		}
		else if (skewCounter == minSkew) {
			minSkewPositions.push_back(i);
		}
		++i;
	}
	return minSkewPositions;
}

int main()
{
	for (const auto& skewPosition : findSkewPositions("input.txt")) {
		cout << skewPosition + 1 << " ";
	}

	return 0;
}
