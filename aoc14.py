recipe_scores = '37'
elf_a_recipe = 0
elf_b_recipe = 1

pattern = '846601'
pattern_len = len(pattern)

num_generations = 846601 + 10

pattern_found = False
while not pattern_found:
    recipe_a_score = int(recipe_scores[elf_a_recipe])
    recipe_b_score = int(recipe_scores[elf_b_recipe])
    new_recipes = recipe_a_score + recipe_b_score
    if new_recipes >= 10:
        recipe_scores += str(new_recipes // 10)
    recipe_scores += str(new_recipes % 10)

    elf_a_recipe = (elf_a_recipe + 1 + recipe_a_score) % len(recipe_scores)
    elf_b_recipe = (elf_b_recipe + 1 + recipe_b_score) % len(recipe_scores)

    if len(recipe_scores) >= (pattern_len + 1) and (recipe_scores[-pattern_len:] == pattern or
                                                    recipe_scores[-pattern_len-1:-1] == pattern):
        pattern_found = True

    print('Finished {} recipes'.format(len(recipe_scores)))

if recipe_scores[-pattern_len:] == pattern:
    print(len(recipe_scores) - pattern_len)
else:
    print(len(recipe_scores) - pattern_len - 1)
