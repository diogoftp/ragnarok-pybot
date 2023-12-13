#include <stdlib.h>
#include <vector>
#include <unordered_set>
#include <map>
#include <string>
#include <stdexcept>
#include <iostream>
#include <queue>
#include <iomanip>
#include <algorithm>
#include <fstream>
#include <iostream>

#ifdef _WIN32
#define DLL_EXPORT __declspec(dllexport)
#else
#define DLL_EXPORT
#endif

#define Point pair<int,int>

using namespace std;

const unordered_set<int> WALKABLE_POS = {0, 3};
const unordered_set<int> VALID_POS = {0, 1, 2, 3, 4, 5, 6, 7};

const vector<int> DX = {-1, 0, 1, 0, -1, -1, 1, 1};
const vector<int> DY = {0, -1, 0, 1, -1, 1, -1, 1};

struct GridMetadata {
    map<pair<Point,Point>, int> dist;
    map<pair<Point,Point>, Point> next;
};

struct PathMetadata {
    int* path;
    size_t size;
};

struct TestInput {
    int* map;
    int row_size, column_size;
    Point start, end;

    TestInput(int* map, int row_size, int column_size, Point start, Point end)
        : map(map), row_size(row_size), column_size(column_size), start(start), end(end) {}
};

struct TestOutput {
    PathMetadata result;

    TestOutput(int* path, size_t size)
        : result{path, size} {}
};

struct TestCase {
    TestInput Input;
    TestOutput Output;

    TestCase(TestInput input, TestOutput output)
        : Input(input), Output(output) {}
};

PathMetadata ShortestPath(int *input, int num_rows, int num_columns, int start_x, int start_y, int end_x, int end_y);

int GetCellNumberFromString(string numberStr) {
    int cellNumber;
    try
    {
        cellNumber = stoi(numberStr);
    }
    catch(const exception& e)
    {
        throw invalid_argument("Failed to parse cell number.\n Expected: [0, 7]\n Got: " + numberStr);
    }

    if(!VALID_POS.count(cellNumber)) {
        throw invalid_argument("Invalid cell number.\n Expected: [0, 7]\n Got: " + numberStr);
    }

    return cellNumber;
}

vector<int> GetCellsListFromString(string line) {
    string number = "";
    vector<int> splited;

    for(int i = 0; i < (int)line.size(); i++) {
        char c = line[i];
        if(c == ',') {
            if(line[i++ + 1] != ' ') {
                throw invalid_argument("Invalid grid format.\n Expected: ', '\n Got: " + c + line[i + 1]);
            }

            splited.push_back(
                GetCellNumberFromString(number)
            );

            number.clear();
        } else {
            number += c;
        }
    }

    return splited;
}

vector<int> LoadMapFromTxt(string file_name) {
    ifstream file(file_name);
    if (!file.is_open()) {
        throw runtime_error("Could not open file");
    }

    string line;
    if (!getline(file, line)) {
        throw logic_error("File is empty");
    }
    file.close();

    return GetCellsListFromString(line);
}

bool CanWalk(Point p, vector<vector<int>> &grid, int num_rows, int num_columns, map<Point, bool> &visited) {
    if(
        p.first < 0 ||
        p.first >= num_rows ||
        p.second < 0 ||
        p.second >= num_columns
    ) return false;
    if(
        visited.count(p) ||
        !WALKABLE_POS.count(grid[p.first][p.second])
    ) return false;

    return true;
}

vector<Point> ExtractPathFromGridMetadata(Point src, Point dst, GridMetadata &data) {
    Point end = {-1, -1};
    Point curr = data.next[{src, dst}];
    vector<Point> path = {dst};

    while(curr != end) {
        path.push_back(curr);
        curr = data.next[{src, curr}];
    }

    // Need to reverse since the path will be from dst to src
    reverse(path.begin(), path.end());

    return path;
}

GridMetadata BFS(Point start, Point end, vector<vector<int>> &grid, int num_rows, int num_columns) {
    queue<Point> q;
    GridMetadata meta_data;
    map<Point, bool> visited;

    q.push(start);
    visited[start] = true;
    meta_data.dist[{start, start}] = 0;
    meta_data.next[{start, start}] = {-1, -1};

    while(!q.empty()) {
        Point src = q.front();
        q.pop();

        for(int i = 0; i < (int)DX.size(); i++) {
            Point newPoint = {src.first + DX[i], src.second + DY[i]};
            if(!CanWalk(newPoint, grid, num_rows, num_columns, visited)) continue;

            meta_data.dist[{start, newPoint}] = meta_data.dist[{start, src}] + 1;
            meta_data.next[{start, newPoint}] = src;
            visited[newPoint] = true;
            q.push(newPoint);

            if(newPoint == end) return meta_data;                
        }
    }

    return meta_data;
}

GridMetadata CalcGridDist(Point start, Point end, vector<vector<int>> grid, int num_rows, int num_columns) {
    return BFS(start, end, grid, num_rows, num_columns);
}

vector<vector<int>> Convert1DTo2DGrid(int *input, int num_rows, int num_columns) {
    vector<int> aux;
    vector<vector<int>> grid;
    vector<int> linearGraph = vector<int>(input, input + (num_rows * num_columns));

    for(int i = 0; i < num_rows; i++) {
        for(int j = 0; j < num_columns; j++) {
            aux.push_back(linearGraph[j * num_rows + i]);
        }
        grid.push_back(aux);
        aux.clear();
    }

    return grid;
}

PathMetadata BuildPathMetadata(vector<Point> &path) {
    PathMetadata meta_data;

    meta_data.size = path.size() * 2;
    meta_data.path = new int[meta_data.size];

    int idx = 0;
    for(const Point &p: path) {
        meta_data.path[idx++] = p.first;
        meta_data.path[idx++] = p.second;
    }

    return meta_data;
}

bool CompareTestCase(PathMetadata expected, PathMetadata got) {
    if(got.size == expected.size) {
        for(int i = 0; i < (int)got.size; i++) {
            if(got.path[i] != expected.path[i]) {
                return false;
            }
        }
    } else {
        return false;
    }

    return true;
}


// ShortestPath test
int main() {
    /*
        2D grid represented as 1D
        Access position (i, j) with formula: map[j * num_rows + i]
    */
    int *map_1 = LoadMapFromTxt("moc_fild13.txt").data();

    /*
        - It's in pair format
        - i and i + 1 represents x,y coordinate
        - You should use:
            {out[0], out[1]},
            {out[2], out[3]},
            {out[4], out[5]},
            ...
    */
    int out_1[] = {
        30, 27, 30, 28, 30, 29, 30, 30, 31, 31, 32, 32, 33, 33, 34, 34, 34, 35, 34, 36, 35, 37, 36, 38, 36, 39, 36, 40,
        36, 41, 36, 42, 36, 43, 36, 44, 36, 45, 36, 46, 36, 47, 36, 48, 36, 49, 36, 50, 36, 51, 36, 52, 36, 53, 36, 54, 
        36, 55, 36, 56, 36, 57, 36, 58, 36, 59, 36, 60, 36, 61, 36, 62, 36, 63, 36, 64, 36, 65, 36, 66, 36, 67, 36, 68, 
        36, 69, 36, 70, 36, 71, 36, 72, 36, 73, 36, 74, 36, 75, 36, 76, 36, 77, 36, 78, 36, 79, 36, 80, 36, 81, 36, 82, 
        36, 83, 36, 84, 36, 85, 36, 86, 36, 87, 36, 88, 36, 89, 36, 90, 36, 91, 36, 92, 36, 93, 36, 94, 36, 95, 36, 96, 
        36, 97, 36, 98, 36, 99, 36, 100, 36, 101, 36, 102, 36, 103, 36, 104, 36, 105, 36, 106, 36, 107, 36, 108, 36, 109,
        36, 110, 36, 111, 36, 112, 36, 113, 36, 114, 36, 115, 36, 116, 36, 117, 36, 118, 36, 119, 36, 120, 36, 121, 36, 
        122, 36, 123, 36, 124, 36, 125, 36, 126, 36, 127, 36, 128, 36, 129, 36, 130, 36, 131, 36, 132, 36, 133, 36, 134, 
        36, 135, 36, 136, 36, 137, 36, 138, 36, 139, 36, 140, 36, 141, 37, 142, 38, 143, 39, 144, 40, 145, 41, 146, 42, 
        147, 43, 148, 44, 149, 45, 150, 46, 151, 47, 152, 48, 153, 49, 154, 50, 155, 51, 156, 52, 157, 52, 158, 52, 159,
        52, 160, 53, 161, 54, 162, 55, 163, 56, 164, 57, 165, 58, 166, 59, 167, 60, 168, 61, 169, 62, 170, 63, 171, 64, 
        172, 65, 173, 66, 174, 67, 175, 68, 176, 69, 177, 70, 178, 71, 179, 72, 180, 73, 181, 74, 182, 75, 183, 76, 184, 
        77, 185, 78, 186, 79, 187, 80, 188, 81, 189, 82, 190, 83, 191, 84, 192, 85, 193
    };

    int out_2[] = {
        46, 151, 46, 150, 46, 149, 46, 148, 46, 147, 46, 146, 46, 145, 46, 144, 46, 143, 46, 142, 46, 141, 46, 140, 46, 
        139, 46, 138, 46, 137, 46, 136, 46, 135, 46, 134, 46, 133, 46, 132, 46, 131, 45, 130, 44, 129, 44, 128, 44, 127, 
        44, 126, 44, 125, 44, 124, 44, 123, 44, 122, 44, 121, 44, 120, 44, 119, 44, 118, 44, 117, 44, 116, 44, 115, 44, 
        114, 44, 113, 44, 112, 44, 111, 44, 110, 44, 109, 44, 108, 44, 107, 44, 106, 44, 105, 44, 104, 44, 103, 44, 102, 
        44, 101, 44, 100, 44, 99, 44, 98, 44, 97, 44, 96, 44, 95, 44, 94, 44, 93, 44, 92, 44, 91, 44, 90, 44, 89, 44, 88, 
        44, 87, 44, 86, 44, 85, 44, 84, 44, 83, 44, 82, 44, 81, 44, 80, 44, 79, 44, 78, 44, 77, 44, 76, 43, 75, 43, 74, 
        43, 73, 43, 72, 43, 71, 43, 70, 43, 69, 43, 68, 43, 67, 43, 66, 43, 65, 43, 64, 43, 63, 43, 62, 42, 61, 42, 60, 
        42, 59, 42, 58, 42, 57, 42, 56, 42, 55, 42, 54, 42, 53, 42, 52, 42, 51, 42, 50, 42, 49, 42, 48, 42, 47, 42, 46, 
        42, 45, 42, 44, 42, 43, 42, 42, 41, 41, 40, 40, 39, 39, 38, 38, 37, 37, 36, 36, 35, 35, 34, 34, 33, 33
    };

    vector<TestCase> input_list = {
        TestCase(
            TestInput(map_1, 340, 400, {30,27}, {85,193}),
            TestOutput(out_1, 334)
        ),
        TestCase(
            TestInput(map_1, 340, 400, {46,151}, {33,33}), 
            TestOutput(out_2, 238)
        ),
        TestCase(
            TestInput(map_1, 340, 400, {0,0}, {1,1}),
            TestOutput(nullptr, 0)
        )
    };

    for(int i = 0; i < (int)input_list.size(); i++) {
        TestCase test_case = input_list[i];
        PathMetadata got = ShortestPath(
            test_case.Input.map, 
            test_case.Input.row_size,
            test_case.Input.column_size,
            test_case.Input.start.first,
            test_case.Input.start.second,
            test_case.Input.end.first,
            test_case.Input.end.second
        );

        printf("Test #%d : %s\n", i + 1, CompareTestCase(test_case.Output.result, got) ? "OK":"FAILED");
    }
}


// Main code
PathMetadata ShortestPath(int *input, int num_rows, int num_columns, int start_x, int start_y, int end_x, int end_y) {
    Point start = {start_x, start_y};
    Point end = {end_x, end_y};

    vector<vector<int>> grid = Convert1DTo2DGrid(input, num_rows, num_columns);

    GridMetadata grid_metadata = CalcGridDist(start, end, grid, num_rows, num_columns);
    if(!grid_metadata.dist.count({start,end})) {
        return PathMetadata{};
    }

    vector<Point> path = ExtractPathFromGridMetadata(start, end, grid_metadata);
    return BuildPathMetadata(path);;
}

extern "C" {
    DLL_EXPORT PathMetadata My_ShortestPath(int *input, int num_rows, int num_columns, int start_x, int start_y, int end_x, int end_y) {
        return ShortestPath(input, num_rows, num_columns, start_x, start_y, end_x, end_y);
    }
}