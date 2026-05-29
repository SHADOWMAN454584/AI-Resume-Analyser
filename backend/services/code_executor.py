"""
Code executor service with sandboxed subprocess execution.
Supports Python and JavaScript (Node.js).
"""
import json
import subprocess
import tempfile
import time
import os
import re

# ---------------------------------------------------------------------------
# Coding Problems Database – 15 problems from Easy to Hard
# ---------------------------------------------------------------------------

CODING_PROBLEMS = [
    {
        "id": "fizzbuzz",
        "title": "FizzBuzz",
        "difficulty": "easy",
        "description": (
            "Write a function `fizzbuzz(n)` that returns a list of strings from 1 to n.\n"
            "For multiples of 3, use 'Fizz'. For multiples of 5, use 'Buzz'.\n"
            "For multiples of both 3 and 5, use 'FizzBuzz'. Otherwise, use the number as a string.\n\n"
            "Example: fizzbuzz(5) → ['1', '2', 'Fizz', '4', 'Buzz']"
        ),
        "starter_code": {
            "python": "def fizzbuzz(n):\n    # Your code here\n    pass\n\n# Read input\nn = int(input())\nprint(fizzbuzz(n))",
            "javascript": "function fizzbuzz(n) {\n    // Your code here\n}\n\n// Read input\nconst n = parseInt(require('fs').readFileSync('/dev/stdin', 'utf8').trim());\nconsole.log(JSON.stringify(fizzbuzz(n)));"
        },
        "test_cases": [
            {"input": "5", "expected_output": "['1', '2', 'Fizz', '4', 'Buzz']"},
            {"input": "15", "expected_output": "['1', '2', 'Fizz', '4', 'Buzz', 'Fizz', '7', '8', 'Fizz', 'Buzz', '11', 'Fizz', '13', '14', 'FizzBuzz']"},
            {"input": "1", "expected_output": "['1']"},
            {"input": "3", "expected_output": "['1', '2', 'Fizz']"}
        ],
        "time_limit": 5
    },
    {
        "id": "palindrome",
        "title": "Palindrome Check",
        "difficulty": "easy",
        "description": (
            "Write a function `is_palindrome(s)` that returns True if the string is a palindrome "
            "(reads the same forwards and backwards), ignoring case and non-alphanumeric characters.\n\n"
            "Example: is_palindrome('A man, a plan, a canal: Panama') → True"
        ),
        "starter_code": {
            "python": "def is_palindrome(s):\n    # Your code here\n    pass\n\n# Read input\ns = input()\nprint(is_palindrome(s))",
            "javascript": "function isPalindrome(s) {\n    // Your code here\n}\n\nconst s = require('fs').readFileSync('/dev/stdin', 'utf8').trim();\nconsole.log(isPalindrome(s));"
        },
        "test_cases": [
            {"input": "A man, a plan, a canal: Panama", "expected_output": "True"},
            {"input": "race a car", "expected_output": "False"},
            {"input": "racecar", "expected_output": "True"},
            {"input": " ", "expected_output": "True"}
        ],
        "time_limit": 5
    },
    {
        "id": "two_sum",
        "title": "Two Sum",
        "difficulty": "easy",
        "description": (
            "Write a function `two_sum(nums, target)` that returns the indices of two numbers "
            "that add up to the target.\n"
            "Input: first line is the target, second line is space-separated numbers.\n"
            "Output: two indices separated by a space.\n\n"
            "Example: target=9, nums=[2,7,11,15] → '0 1'"
        ),
        "starter_code": {
            "python": "def two_sum(nums, target):\n    # Your code here\n    pass\n\ntarget = int(input())\nnums = list(map(int, input().split()))\nresult = two_sum(nums, target)\nprint(f'{result[0]} {result[1]}')",
            "javascript": "function twoSum(nums, target) {\n    // Your code here\n}\n\nconst lines = require('fs').readFileSync('/dev/stdin', 'utf8').trim().split('\\n');\nconst target = parseInt(lines[0]);\nconst nums = lines[1].split(' ').map(Number);\nconst result = twoSum(nums, target);\nconsole.log(`${result[0]} ${result[1]}`);"
        },
        "test_cases": [
            {"input": "9\n2 7 11 15", "expected_output": "0 1"},
            {"input": "6\n3 2 4", "expected_output": "1 2"},
            {"input": "6\n3 3", "expected_output": "0 1"}
        ],
        "time_limit": 5
    },
    {
        "id": "reverse_linked_list",
        "title": "Reverse a String",
        "difficulty": "easy",
        "description": (
            "Write a function `reverse_string(s)` that reverses a string without using "
            "built-in reverse functions.\n\n"
            "Example: reverse_string('hello') → 'olleh'"
        ),
        "starter_code": {
            "python": "def reverse_string(s):\n    # Your code here\n    pass\n\ns = input()\nprint(reverse_string(s))",
            "javascript": "function reverseString(s) {\n    // Your code here\n}\n\nconst s = require('fs').readFileSync('/dev/stdin', 'utf8').trim();\nconsole.log(reverseString(s));"
        },
        "test_cases": [
            {"input": "hello", "expected_output": "olleh"},
            {"input": "world", "expected_output": "dlrow"},
            {"input": "a", "expected_output": "a"},
            {"input": "ab", "expected_output": "ba"}
        ],
        "time_limit": 5
    },
    {
        "id": "valid_parentheses",
        "title": "Valid Parentheses",
        "difficulty": "easy",
        "description": (
            "Write a function `is_valid(s)` that determines if a string of brackets is valid.\n"
            "Valid means every open bracket is closed by the same type in the correct order.\n"
            "Bracket types: (), {}, []\n\n"
            "Example: is_valid('()[]{}') → True\n"
            "Example: is_valid('(]') → False"
        ),
        "starter_code": {
            "python": "def is_valid(s):\n    # Your code here\n    pass\n\ns = input()\nprint(is_valid(s))",
            "javascript": "function isValid(s) {\n    // Your code here\n}\n\nconst s = require('fs').readFileSync('/dev/stdin', 'utf8').trim();\nconsole.log(isValid(s));"
        },
        "test_cases": [
            {"input": "()[]{}", "expected_output": "True"},
            {"input": "(]", "expected_output": "False"},
            {"input": "([)]", "expected_output": "False"},
            {"input": "{[]}", "expected_output": "True"},
            {"input": "", "expected_output": "True"}
        ],
        "time_limit": 5
    },
    {
        "id": "max_subarray",
        "title": "Maximum Subarray Sum",
        "difficulty": "medium",
        "description": (
            "Write a function `max_subarray(nums)` that finds the contiguous subarray "
            "with the largest sum and returns that sum.\n"
            "Input: space-separated integers.\n\n"
            "Example: max_subarray([-2,1,-3,4,-1,2,1,-5,4]) → 6 (subarray [4,-1,2,1])"
        ),
        "starter_code": {
            "python": "def max_subarray(nums):\n    # Your code here\n    pass\n\nnums = list(map(int, input().split()))\nprint(max_subarray(nums))",
            "javascript": "function maxSubarray(nums) {\n    // Your code here\n}\n\nconst nums = require('fs').readFileSync('/dev/stdin', 'utf8').trim().split(' ').map(Number);\nconsole.log(maxSubarray(nums));"
        },
        "test_cases": [
            {"input": "-2 1 -3 4 -1 2 1 -5 4", "expected_output": "6"},
            {"input": "1", "expected_output": "1"},
            {"input": "5 4 -1 7 8", "expected_output": "23"},
            {"input": "-1", "expected_output": "-1"}
        ],
        "time_limit": 5
    },
    {
        "id": "binary_search",
        "title": "Binary Search",
        "difficulty": "medium",
        "description": (
            "Write a function `binary_search(nums, target)` that returns the index of "
            "target in a sorted array, or -1 if not found.\n"
            "Input: first line is the target, second line is space-separated sorted numbers.\n\n"
            "Example: binary_search([1,3,5,7,9], 5) → 2"
        ),
        "starter_code": {
            "python": "def binary_search(nums, target):\n    # Your code here\n    pass\n\ntarget = int(input())\nnums = list(map(int, input().split()))\nprint(binary_search(nums, target))",
            "javascript": "function binarySearch(nums, target) {\n    // Your code here\n}\n\nconst lines = require('fs').readFileSync('/dev/stdin', 'utf8').trim().split('\\n');\nconst target = parseInt(lines[0]);\nconst nums = lines[1].split(' ').map(Number);\nconsole.log(binarySearch(nums, target));"
        },
        "test_cases": [
            {"input": "5\n1 3 5 7 9", "expected_output": "2"},
            {"input": "2\n1 3 5 7 9", "expected_output": "-1"},
            {"input": "1\n1", "expected_output": "0"},
            {"input": "9\n1 3 5 7 9", "expected_output": "4"}
        ],
        "time_limit": 5
    },
    {
        "id": "anagram_check",
        "title": "Anagram Check",
        "difficulty": "medium",
        "description": (
            "Write a function `is_anagram(s, t)` that returns True if t is an anagram of s.\n"
            "Input: two lines, one string each.\n\n"
            "Example: is_anagram('anagram', 'nagaram') → True"
        ),
        "starter_code": {
            "python": "def is_anagram(s, t):\n    # Your code here\n    pass\n\ns = input()\nt = input()\nprint(is_anagram(s, t))",
            "javascript": "function isAnagram(s, t) {\n    // Your code here\n}\n\nconst lines = require('fs').readFileSync('/dev/stdin', 'utf8').trim().split('\\n');\nconsole.log(isAnagram(lines[0], lines[1]));"
        },
        "test_cases": [
            {"input": "anagram\nnagaram", "expected_output": "True"},
            {"input": "rat\ncar", "expected_output": "False"},
            {"input": "listen\nsilent", "expected_output": "True"},
            {"input": "a\na", "expected_output": "True"}
        ],
        "time_limit": 5
    },
    {
        "id": "flatten_array",
        "title": "Flatten Nested Array",
        "difficulty": "medium",
        "description": (
            "Write a function `flatten(arr)` that takes a nested list/array and returns "
            "a flat list of all elements.\n"
            "Input: a JSON array (may be nested).\n\n"
            "Example: flatten([1,[2,[3,4],5],6]) → [1,2,3,4,5,6]"
        ),
        "starter_code": {
            "python": "import json\n\ndef flatten(arr):\n    # Your code here\n    pass\n\narr = json.loads(input())\nprint(json.dumps(flatten(arr)))",
            "javascript": "function flatten(arr) {\n    // Your code here\n}\n\nconst arr = JSON.parse(require('fs').readFileSync('/dev/stdin', 'utf8').trim());\nconsole.log(JSON.stringify(flatten(arr)));"
        },
        "test_cases": [
            {"input": "[1,[2,[3,4],5],6]", "expected_output": "[1, 2, 3, 4, 5, 6]"},
            {"input": "[[1,2],[3,4]]", "expected_output": "[1, 2, 3, 4]"},
            {"input": "[1,2,3]", "expected_output": "[1, 2, 3]"},
            {"input": "[[[[1]]]]", "expected_output": "[1]"}
        ],
        "time_limit": 5
    },
    {
        "id": "longest_substring",
        "title": "Longest Substring Without Repeating Characters",
        "difficulty": "medium",
        "description": (
            "Write a function `length_of_longest_substring(s)` that returns the length of "
            "the longest substring without repeating characters.\n\n"
            "Example: length_of_longest_substring('abcabcbb') → 3"
        ),
        "starter_code": {
            "python": "def length_of_longest_substring(s):\n    # Your code here\n    pass\n\ns = input()\nprint(length_of_longest_substring(s))",
            "javascript": "function lengthOfLongestSubstring(s) {\n    // Your code here\n}\n\nconst s = require('fs').readFileSync('/dev/stdin', 'utf8').trim();\nconsole.log(lengthOfLongestSubstring(s));"
        },
        "test_cases": [
            {"input": "abcabcbb", "expected_output": "3"},
            {"input": "bbbbb", "expected_output": "1"},
            {"input": "pwwkew", "expected_output": "3"},
            {"input": " ", "expected_output": "1"}
        ],
        "time_limit": 5
    },
    {
        "id": "merge_sorted_arrays",
        "title": "Merge Two Sorted Arrays",
        "difficulty": "medium",
        "description": (
            "Write a function `merge_sorted(arr1, arr2)` that merges two sorted arrays "
            "into one sorted array.\n"
            "Input: two lines of space-separated integers.\n\n"
            "Example: merge_sorted([1,3,5], [2,4,6]) → [1,2,3,4,5,6]"
        ),
        "starter_code": {
            "python": "import json\n\ndef merge_sorted(arr1, arr2):\n    # Your code here\n    pass\n\narr1 = list(map(int, input().split()))\narr2 = list(map(int, input().split()))\nprint(json.dumps(merge_sorted(arr1, arr2)))",
            "javascript": "function mergeSorted(arr1, arr2) {\n    // Your code here\n}\n\nconst lines = require('fs').readFileSync('/dev/stdin', 'utf8').trim().split('\\n');\nconst arr1 = lines[0].split(' ').map(Number);\nconst arr2 = lines[1].split(' ').map(Number);\nconsole.log(JSON.stringify(mergeSorted(arr1, arr2)));"
        },
        "test_cases": [
            {"input": "1 3 5\n2 4 6", "expected_output": "[1, 2, 3, 4, 5, 6]"},
            {"input": "1 2 3\n4 5 6", "expected_output": "[1, 2, 3, 4, 5, 6]"},
            {"input": "1\n2", "expected_output": "[1, 2]"}
        ],
        "time_limit": 5
    },
    {
        "id": "merge_intervals",
        "title": "Merge Intervals",
        "difficulty": "hard",
        "description": (
            "Write a function `merge_intervals(intervals)` that merges all overlapping intervals.\n"
            "Input: JSON array of [start, end] pairs.\n\n"
            "Example: merge_intervals([[1,3],[2,6],[8,10],[15,18]]) → [[1,6],[8,10],[15,18]]"
        ),
        "starter_code": {
            "python": "import json\n\ndef merge_intervals(intervals):\n    # Your code here\n    pass\n\nintervals = json.loads(input())\nprint(json.dumps(merge_intervals(intervals)))",
            "javascript": "function mergeIntervals(intervals) {\n    // Your code here\n}\n\nconst intervals = JSON.parse(require('fs').readFileSync('/dev/stdin', 'utf8').trim());\nconsole.log(JSON.stringify(mergeIntervals(intervals)));"
        },
        "test_cases": [
            {"input": "[[1,3],[2,6],[8,10],[15,18]]", "expected_output": "[[1, 6], [8, 10], [15, 18]]"},
            {"input": "[[1,4],[4,5]]", "expected_output": "[[1, 5]]"},
            {"input": "[[1,4],[2,3]]", "expected_output": "[[1, 4]]"}
        ],
        "time_limit": 5
    },
    {
        "id": "lru_cache",
        "title": "LRU Cache",
        "difficulty": "hard",
        "description": (
            "Implement an LRU (Least Recently Used) cache with get and put operations.\n"
            "Input: first line is capacity, subsequent lines are operations:\n"
            "  'put key value' or 'get key'\n"
            "For get, print the value or -1 if not found.\n\n"
            "Example:\n  capacity=2\n  put 1 1\n  put 2 2\n  get 1 → 1\n  put 3 3 (evicts key 2)\n  get 2 → -1"
        ),
        "starter_code": {
            "python": (
                "class LRUCache:\n"
                "    def __init__(self, capacity):\n"
                "        # Your code here\n"
                "        pass\n\n"
                "    def get(self, key):\n"
                "        # Your code here\n"
                "        pass\n\n"
                "    def put(self, key, value):\n"
                "        # Your code here\n"
                "        pass\n\n"
                "import sys\n"
                "lines = sys.stdin.read().strip().split('\\n')\n"
                "capacity = int(lines[0])\n"
                "cache = LRUCache(capacity)\n"
                "for line in lines[1:]:\n"
                "    parts = line.split()\n"
                "    if parts[0] == 'put':\n"
                "        cache.put(int(parts[1]), int(parts[2]))\n"
                "    elif parts[0] == 'get':\n"
                "        print(cache.get(int(parts[1])))\n"
            ),
            "javascript": (
                "class LRUCache {\n"
                "    constructor(capacity) {\n"
                "        // Your code here\n"
                "    }\n"
                "    get(key) {\n"
                "        // Your code here\n"
                "    }\n"
                "    put(key, value) {\n"
                "        // Your code here\n"
                "    }\n"
                "}\n\n"
                "const lines = require('fs').readFileSync('/dev/stdin', 'utf8').trim().split('\\n');\n"
                "const capacity = parseInt(lines[0]);\n"
                "const cache = new LRUCache(capacity);\n"
                "for (let i = 1; i < lines.length; i++) {\n"
                "    const parts = lines[i].split(' ');\n"
                "    if (parts[0] === 'put') {\n"
                "        cache.put(parseInt(parts[1]), parseInt(parts[2]));\n"
                "    } else if (parts[0] === 'get') {\n"
                "        console.log(cache.get(parseInt(parts[1])));\n"
                "    }\n"
                "}\n"
            )
        },
        "test_cases": [
            {
                "input": "2\nput 1 1\nput 2 2\nget 1\nput 3 3\nget 2",
                "expected_output": "1\n-1"
            },
            {
                "input": "1\nput 1 10\nget 1\nput 2 20\nget 1\nget 2",
                "expected_output": "10\n-1\n20"
            }
        ],
        "time_limit": 10
    },
    {
        "id": "spiral_matrix",
        "title": "Spiral Matrix Traversal",
        "difficulty": "hard",
        "description": (
            "Write a function `spiral_order(matrix)` that returns all elements of a matrix "
            "in spiral order (clockwise from top-left).\n"
            "Input: JSON 2D array.\n\n"
            "Example: spiral_order([[1,2,3],[4,5,6],[7,8,9]]) → [1,2,3,6,9,8,7,4,5]"
        ),
        "starter_code": {
            "python": "import json\n\ndef spiral_order(matrix):\n    # Your code here\n    pass\n\nmatrix = json.loads(input())\nprint(json.dumps(spiral_order(matrix)))",
            "javascript": "function spiralOrder(matrix) {\n    // Your code here\n}\n\nconst matrix = JSON.parse(require('fs').readFileSync('/dev/stdin', 'utf8').trim());\nconsole.log(JSON.stringify(spiralOrder(matrix)));"
        },
        "test_cases": [
            {"input": "[[1,2,3],[4,5,6],[7,8,9]]", "expected_output": "[1, 2, 3, 6, 9, 8, 7, 4, 5]"},
            {"input": "[[1,2,3,4],[5,6,7,8],[9,10,11,12]]", "expected_output": "[1, 2, 3, 4, 8, 12, 11, 10, 9, 5, 6, 7]"},
            {"input": "[[1]]", "expected_output": "[1]"}
        ],
        "time_limit": 5
    },
    {
        "id": "count_islands",
        "title": "Number of Islands",
        "difficulty": "hard",
        "description": (
            "Write a function `num_islands(grid)` that counts the number of islands in a "
            "2D grid. '1' represents land, '0' represents water. An island is surrounded "
            "by water and connected horizontally or vertically.\n"
            "Input: JSON 2D array of strings.\n\n"
            "Example: num_islands([['1','1','0'],['0','1','0'],['0','0','1']]) → 2"
        ),
        "starter_code": {
            "python": "import json\n\ndef num_islands(grid):\n    # Your code here\n    pass\n\ngrid = json.loads(input())\nprint(num_islands(grid))",
            "javascript": "function numIslands(grid) {\n    // Your code here\n}\n\nconst grid = JSON.parse(require('fs').readFileSync('/dev/stdin', 'utf8').trim());\nconsole.log(numIslands(grid));"
        },
        "test_cases": [
            {
                "input": '[[\"1\",\"1\",\"1\",\"1\",\"0\"],[\"1\",\"1\",\"0\",\"1\",\"0\"],[\"1\",\"1\",\"0\",\"0\",\"0\"],[\"0\",\"0\",\"0\",\"0\",\"0\"]]',
                "expected_output": "1"
            },
            {
                "input": '[[\"1\",\"1\",\"0\",\"0\",\"0\"],[\"1\",\"1\",\"0\",\"0\",\"0\"],[\"0\",\"0\",\"1\",\"0\",\"0\"],[\"0\",\"0\",\"0\",\"1\",\"1\"]]',
                "expected_output": "3"
            }
        ],
        "time_limit": 10
    }
]

# Build a lookup dict by problem ID
_PROBLEMS_BY_ID = {p['id']: p for p in CODING_PROBLEMS}


def get_problem(problem_id):
    """Get a coding problem by ID."""
    return _PROBLEMS_BY_ID.get(problem_id)


def get_all_problems(include_expected=False):
    """
    Return all problems. Optionally strip expected_output for security.

    Args:
        include_expected: If False, removes expected_output from test cases.

    Returns:
        List of problem dicts.
    """
    problems = []
    for p in CODING_PROBLEMS:
        prob = {
            'id': p['id'],
            'title': p['title'],
            'difficulty': p['difficulty'],
            'description': p['description'],
            'starter_code': p['starter_code'],
            'time_limit': p['time_limit'],
            'test_case_count': len(p['test_cases'])
        }
        if include_expected:
            prob['test_cases'] = p['test_cases']
        else:
            # Only show inputs, not expected outputs
            prob['test_cases'] = [{'input': tc['input']} for tc in p['test_cases']]
        problems.append(prob)
    return problems


def execute_code(code, language, test_cases, time_limit=10):
    """
    Execute code against test cases in a sandboxed subprocess.

    Args:
        code: Source code string.
        language: 'python' or 'javascript'.
        test_cases: List of dicts with 'input' and 'expected_output'.
        time_limit: Maximum execution time in seconds per test case.

    Returns:
        Dict with passed, total, results, execution_time, error.
    """
    if language not in ('python', 'javascript'):
        return {
            'passed': 0,
            'total': len(test_cases),
            'results': [],
            'execution_time': 0,
            'error': f'Unsupported language: {language}'
        }

    results = []
    total_passed = 0
    total_time = 0.0
    global_error = None

    for tc in test_cases:
        tc_input = tc.get('input', '')
        expected = tc.get('expected_output', '').strip()

        try:
            actual, exec_time, error = _run_single(code, language, tc_input, time_limit)
            total_time += exec_time

            if error:
                results.append({
                    'input': tc_input,
                    'expected': expected,
                    'actual': '',
                    'passed': False,
                    'error': error
                })
            else:
                actual_stripped = actual.strip()
                passed = _compare_output(actual_stripped, expected)
                if passed:
                    total_passed += 1
                results.append({
                    'input': tc_input,
                    'expected': expected,
                    'actual': actual_stripped,
                    'passed': passed,
                    'error': None
                })
        except Exception as e:
            results.append({
                'input': tc_input,
                'expected': expected,
                'actual': '',
                'passed': False,
                'error': str(e)
            })

    return {
        'passed': total_passed,
        'total': len(test_cases),
        'results': results,
        'execution_time': round(total_time, 3),
        'error': global_error
    }


def _run_single(code, language, stdin_input, time_limit):
    """
    Run code once with given stdin input.

    Returns:
        Tuple of (stdout, execution_time, error_message_or_None).
    """
    suffix = '.py' if language == 'python' else '.js'

    # Create a temp file with the code
    tmp_dir = tempfile.mkdtemp()
    tmp_file = os.path.join(tmp_dir, f'solution{suffix}')

    try:
        with open(tmp_file, 'w', encoding='utf-8') as f:
            f.write(code)

        if language == 'python':
            cmd = ['python', tmp_file]
        else:
            cmd = ['node', tmp_file]

        start_time = time.time()
        proc = subprocess.run(
            cmd,
            input=stdin_input,
            capture_output=True,
            text=True,
            timeout=time_limit,
            cwd=tmp_dir,
            env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'}
        )
        exec_time = time.time() - start_time

        if proc.returncode != 0:
            stderr = proc.stderr.strip()
            # Sanitize file paths from error messages
            stderr = stderr.replace(tmp_file, '<solution>')
            stderr = stderr.replace(tmp_dir, '<dir>')
            return '', exec_time, f'Runtime Error: {stderr[:500]}'

        return proc.stdout, exec_time, None

    except subprocess.TimeoutExpired:
        return '', time_limit, f'Time Limit Exceeded ({time_limit}s)'
    except FileNotFoundError:
        interpreter = 'Python' if language == 'python' else 'Node.js'
        return '', 0, f'{interpreter} is not installed or not in PATH'
    except Exception as e:
        return '', 0, f'Execution error: {str(e)[:300]}'
    finally:
        # Cleanup
        try:
            if os.path.exists(tmp_file):
                os.remove(tmp_file)
            if os.path.exists(tmp_dir):
                os.rmdir(tmp_dir)
        except OSError:
            pass


def _compare_output(actual, expected):
    """
    Compare actual output with expected output.
    Handles minor formatting differences.
    """
    if actual == expected:
        return True

    # Normalize whitespace
    actual_norm = ' '.join(actual.split())
    expected_norm = ' '.join(expected.split())
    if actual_norm == expected_norm:
        return True

    # Try comparing as JSON (handles spacing in arrays/objects)
    try:
        actual_json = json.loads(actual)
        expected_json = json.loads(expected)
        if actual_json == expected_json:
            return True
    except (json.JSONDecodeError, TypeError):
        pass

    # Case-insensitive comparison for boolean-like outputs
    if actual.lower() == expected.lower():
        return True

    return False
