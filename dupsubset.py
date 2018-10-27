class Solution(object):
    def generate_subset_size(self, subsets, nums, queue, start_idx, size, num_val):
        subsets.append(queue)
        for num_idx in xrange(start_idx, num_val):
            cur_val = nums[num_idx]
            if num_idx == start_idx or cur_val != nums[num_idx - 1]:
                self.generate_subset_size(subsets, nums, queue + [cur_val], num_idx + 1, size + 1, num_val)

    def subsetsWithDup(self, nums):
        """
        :type nums: List[int]
        :rtype: List[List[int]]
        """
        subsets = list()
        nums.sort()
        num_val = len(nums)

        self.generate_subset_size(subsets, nums, [], 0, 1, num_val)

        return subsets


solution = Solution()
#print(solution.subsetsWithDup([1, 2, 2]))
#print(solution.subsetsWithDup([1, 2, 3, 4]))
#print(solution.subsetsWithDup([1, 2, 2, 3, 4]))
print(solution.subsetsWithDup([4, 4, 4, 1, 4]))