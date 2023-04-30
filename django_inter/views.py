from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import nltk
import json
from nltk import Tree
from copy import deepcopy
from itertools import product, permutations
import itertools
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET


@csrf_exempt
@require_GET
def paraphrase(request):


    # tree_string = "(S (NP (NP (DT The) (JJ charming) (NNP Gothic) (NNP Quarter)) (, ,) (CC or) (NP (NNP Barri) (NNP Gòtic))) (, ,) (VP (VBZ has) (NP (NP (JJ narrow) (JJ medieval) (NNS streets)) (VP (VBN filled) (PP (IN with) (NP (NP (JJ trendy) (NNS bars)) (, ,) (NP (NNS clubs)) (CC and) (NP (JJ Catalan) (NNS restaurants))))))))"
    def new_combination(listy):
        return (list(itertools.product(*listy)))

    def p_combination(*listu):
        result = []
        temp = []
        for i in list(*listu):
            for item in permutations(i):
                temp.append(item)
            result.append(deepcopy(temp))
            temp.clear()
        return result

    def permute_nouns(tree):
        result = []
        # if not isinstance(tree, Tree):
        #     return "net"
        tree = Tree.fromstring(tree)
        if isinstance(tree, Tree):
            #tree = Tree.fromstring(tree)
            temp_position = []
            temp = []
            change_item = []
            change_position = []
            for subtree in tree.subtrees():
                if subtree.label() == "NP":
                    for subsubtree in subtree:
                        if subsubtree.label() == "NP":
                            for subsubsubtree in subsubtree:
                                if subsubsubtree.label() == "NNS" or subsubsubtree.label() == "NNP":
                                    temp.append(subsubtree)
                                    for position in tree.treepositions():
                                        pos = tree[position]
                                        poss = subsubtree
                                        if pos == poss:
                                            temp_position.append(position)
                    if len(temp) > 1:

                        m = 0
                        while m < len(temp) - 1:
                            if temp[m] == temp[m + 1]:
                                temp.pop(m)
                            m += 1
                        n = 0
                        while n < len(temp_position) - 1:
                            if temp_position[n] == temp_position[n + 1]:
                                temp_position.pop(n)
                            n += 1
                        change_item.append(deepcopy(temp))
                        change_position.append(deepcopy(temp_position))
                    temp.clear()
                    temp_position.clear()

            k = 0
            while k < len(change_item) - 1:
                if change_item[k] == change_item[k + 1]:
                    change_item.pop(k)
                k += 1

            j = 0
            while j < len(change_position) - 1:
                if change_position[j] == change_position[j + 1]:
                    change_position.pop(j)
                j += 1

            # combinations variations
            changed_items = p_combination(change_item)
            perm_items = new_combination(changed_items)

            # new tree

            temp_tree = (deepcopy(tree))
            for item in perm_items:
                index_item = 0
                for ind_item in item:
                    index_item_pos = 0
                    for i in ind_item:
                        poss = change_position[index_item][index_item_pos]
                        temp_tree[poss] = Tree.fromstring(str(i))
                        index_item_pos += 1
                        result.append(deepcopy(temp_tree))

                    index_item += 1

            # delete copy

            def delete_copy(result):
                index_sentence = 0
                while index_sentence < len(result) - 1:
                    if result[index_sentence] == result[index_sentence + 1]:
                        result.pop(index_sentence)
                    index_sentence += 1
                return result

            def delete_cop(result):
                temp_result = []
                for ii in result:
                    if ii not in temp_result:
                        temp_result.append(ii)
                return temp_result

            # delete wrong

            def delete_func(result):
                for sentense in result:
                    flag = False
                    for r_subtree in sentense.subtrees():
                        amount = 0
                        for r_next_subtree in sentense.subtrees():
                            if r_subtree == r_next_subtree:
                                if r_subtree.label() == 'NP' or r_subtree.label() == 'NNS':
                                    amount += 1
                                    if amount > 1:
                                        result.remove(sentense)
                                        flag = True
                                        break
                        if flag:
                            flag = False
                            break
                    if flag:
                        break
                return result

            temp_result = delete_cop(result)
            delete_func(temp_result)
            delete_func(temp_result)

            def not_input(result, tree):
                for i in result:
                    if i == tree:
                        result.remove(i)
                return result

            end_result = not_input(temp_result, tree)

            return end_result


        else:
            return "Not tree"

    if request.method == "GET":

        input_tree = request.GET.get('tree', None)
        limit = int(request.GET.get('limit', 20))


        paraphrased_trees = permute_nouns(input_tree)
        new_dict = {}
        n=0
        for element in paraphrased_trees:

            new_dict[f"tree{n}"] = element
            n += 1


        response_data = {

            "paraphrased": new_dict

        }



    return JsonResponse(response_data)