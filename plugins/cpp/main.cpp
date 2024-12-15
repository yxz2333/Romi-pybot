#include <iostream>
#include <algorithm>
#include <random>
#include <string>
#include <vector>
#include <set>
#include <map>
#include <unordered_map>
#include <unordered_set>
#include <json.hpp>
#include <pybind11/pybind11.h>
#define fa(i,op,n) for (int i = op; i <= n; i++)
#define fb(j,op,n) for (int j = op; j >= n; j--)
#define HashMap unordered_map
#define HashSet unordered_set
#define var auto
namespace py = pybind11;
namespace nlo = nlohmann;
using json = nlo::json;

// 错误处理
json ERROR = { { "error", "error" } };
json CANNOT_FOUND = { { "error", "cannot found" } };


// 随机数生成器引擎
std::mt19937 generator(std::random_device{}());



// 获取一个人全部 ac 的题
// 传入一个 json，返回 ac 的题的 problem_id
// https://kenkoooo.com/atcoder/atcoder-api/v3/user/submissions?user=yxz2333&from_second=0
std::HashSet<std::string> get_all_ac(
	const json& data)
{
	var se = std::HashSet<std::string>();
	for (const var& item : data) {
		var result = item.value("result", "Unknown");
		if (
			result == "AC" and
			item.value("problem_id", "Unknown") != "Unknown"
			)
			se.insert(item["problem_id"]);
	}
	return se;
}


// json：获取 at 上所有的 {index} 题
// 传入一个 json
// https://kenkoooo.com/atcoder/resources/problems.json
std::vector<json> all_problems_by_index(
	const json& data,
	const std::string& contest_type,
	const std::string& index)
{
	var ve = std::vector<json>();
	for (const var& item : data) {
		var problem_index = item.value("problem_index", "Unknown");
		var problem_id = item.value("id", "Unknown");
		if (
			problem_index == index and
			problem_id.find(contest_type) != std::string::npos
			)
			ve.push_back(item);
	}
	return ve;
}


std::string get_random_problem_by_index(
	const std::string& all_problems,    // at 上的所有题
	const std::string& all_submissions, // 用户的所有提交
	const std::string& contest_type,
	const std::string& index,
	bool can_aced = 0)
{
	try {
		var all_problems_json = json::parse(all_problems);

		// 按 index 和 contest_type 筛选后的 problems
		var index_problems = all_problems_by_index(all_problems_json, contest_type, index);

		if (can_aced) { // 可以是已经 ac 过的题
			int n = index_problems.size();
			if (n == 0)return CANNOT_FOUND.dump();

			std::uniform_int_distribution<int>
				distribution(0, n);
			int random_num = distribution(generator);

			return index_problems[random_num].dump();
		}
		else { // 不能是已经 ac 过的题
			var all_submissions_json = json::parse(all_submissions);

			// 用户 ac 的 problems
			std::HashSet<std::string>
				ac_problems = get_all_ac(all_submissions_json);

			// 最后筛选的可抽的值 (index_problems - ac_problems)
			var final_problems = std::vector<json>();
			for (const var& item : index_problems) {
				var name = item.value("id", "Unknown");
				if (name != "Unknown" and ac_problems.count(name) == 0)
					final_problems.push_back(item);
			}

			int n = final_problems.size();
			if (n == 0)return CANNOT_FOUND.dump();

			// 生成随机数进行抽题
			std::uniform_int_distribution<int>
				distribution(0, n);
			int random_num = distribution(generator);

			return final_problems[random_num].dump();
		}
	}
	catch (const std::exception& e) {
		std::cerr << "Error: " << e.what() << std::endl;
		return ERROR.dump();
	}
}


// 传入两个 json，即两组队伍分组所有人的的所有提交
// 传入是否重复
std::string get_duel_problem_by_index(
	const std::string& all_problems,
	const std::vector<std::string>& team_1,
	const std::vector<std::string>& team_2,
	const std::string& contest_type,
	const std::string& index,
	bool can_aced = 0)
{

}


PYBIND11_MODULE(atcoder_cpp_api, m) {
	m.doc() = "atcoder module cpp api";
	m.def("get_random_problem_by_index", &get_random_problem_by_index, "Pick questions from AtCoder.");
}