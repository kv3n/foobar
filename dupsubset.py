class Solution(object):
    def generate_subset_size(self, subsets, nums, queue, start_idx):
        num_val = len(nums)
        end_idx = (num_val - 1)
        if start_idx == num_val:
            subsets.append(queue)
            return

        next_idx = start_idx
        next_val = nums[next_idx]
        while next_idx < end_idx and next_val == nums[next_idx + 1]:
            next_idx += 1
            next_val = nums[next_idx]
        next_idx += 1

        cur_val = nums[start_idx]
        self.generate_subset_size(subsets, nums, queue, next_idx)
        self.generate_subset_size(subsets, nums, queue + [cur_val], next_idx)

        for rep_size in xrange(2, next_idx - start_idx + 1):
            self.generate_subset_size(subsets, nums, queue + ([cur_val] * rep_size), next_idx)

    def subsetsWithDup(self, nums):
        """
        :type nums: List[int]
        :rtype: List[List[int]]
        """
        subsets = list()
        nums.sort()

        self.generate_subset_size(subsets, nums, [], 0)

        return subsets


solution = Solution()
#print(solution.subsetsWithDup([1, 1]))
print(solution.subsetsWithDup([1, 2, 2]))
#print(solution.subsetsWithDup([1, 2, 3, 4]))
#print(solution.subsetsWithDup([1, 2, 2, 3, 4]))
#print(solution.subsetsWithDup([4, 4, 4, 1, 4]))