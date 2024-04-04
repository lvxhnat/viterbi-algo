from collections import defaultdict
import math

def naive_predict(in_output_probs_filename, in_test_filename, out_prediction_filename):
    delta = 0.1
    tag_word_counts = defaultdict(lambda: defaultdict(int))
    tag_counts = defaultdict(int)
    word_set = set()
    
    with open(in_output_probs_filename, 'r') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) == 2:
                word, tag = parts
                tag_word_counts[tag][word] += 1
                tag_counts[tag] += 1
                word_set.add(word)
    
    num_words = len(word_set)
    
    with open(out_prediction_filename, 'w') as f:
        for tag in tag_word_counts:
            for word in tag_word_counts[tag]:
                smoothed_prob = (tag_word_counts[tag][word] + delta) / (tag_counts[tag] + delta * (num_words + 1))
                f.write(f"{tag} {word} {smoothed_prob}\n")
                
def naive_predict2(in_output_probs_filename, in_train_filename, in_test_filename, out_prediction_filename):
    probs = defaultdict(dict)
    with open(in_output_probs_filename, 'r') as f:
        for line in f:
            tag, word, prob = line.strip().split()
            probs[word][tag] = float(prob)
    
    with open(in_test_filename, 'r') as test_f, open(out_prediction_filename, 'w') as pred_f:
        for line in test_f:
            word = line.strip()
            if word: 
                best_tag, best_prob = max(probs.get(word, {}).items(), key=lambda x: x[1], default=("@", 0))
                pred_f.write(f"{best_tag}\n")
            else:
                pred_f.write("\n") 

def viterbi_predict(in_tags_filename, in_trans_probs_filename, in_output_probs_filename, in_test_filename, out_predictions_filename):
    pass

def viterbi_predict2(in_tags_filename, in_trans_probs_filename, in_output_probs_filename, in_test_filename,
                     out_predictions_filename):
    pass




def evaluate(in_prediction_filename, in_answer_filename):
    """Do not change this method"""
    with open(in_prediction_filename) as fin:
        predicted_tags = [l.strip() for l in fin.readlines() if len(l.strip()) != 0]

    with open(in_answer_filename) as fin:
        ground_truth_tags = [l.strip() for l in fin.readlines() if len(l.strip()) != 0]

    assert len(predicted_tags) == len(ground_truth_tags)
    correct = 0
    for pred, truth in zip(predicted_tags, ground_truth_tags):
        if pred == truth: correct += 1
    return correct, len(predicted_tags), correct/len(predicted_tags)



def run():
    '''
    You should not have to change the code in this method. We will use it to execute and evaluate your code.
    You can of course comment out the parts that are not relevant to the task that you are working on, but make sure to
    uncomment them later.
    This sequence of code corresponds to the sequence of questions in your project handout.
    '''

    ddir = '/Users/lohyikuang/Downloads/school_semesters/2024 Y3 SEMESTER 2/BT 3102/final_project/project_files' 

    in_train_filename = f'{ddir}/twitter_train.txt'

    naive_output_probs_filename = f'{ddir}/naive_output_probs.txt'

    in_test_filename = f'{ddir}/twitter_dev_no_tag.txt'
    in_ans_filename  = f'{ddir}/twitter_dev_ans.txt'
    naive_prediction_filename = f'{ddir}/naive_predictions.txt'
    naive_predict(naive_output_probs_filename, in_test_filename, naive_prediction_filename)
    correct, total, acc = evaluate(naive_prediction_filename, in_ans_filename)
    print(f'Naive prediction accuracy:     {correct}/{total} = {acc}')

    naive_prediction_filename2 = f'{ddir}/naive_predictions2.txt'
    naive_predict2(naive_output_probs_filename, in_train_filename, in_test_filename, naive_prediction_filename2)
    correct, total, acc = evaluate(naive_prediction_filename2, in_ans_filename)
    print(f'Naive prediction2 accuracy:    {correct}/{total} = {acc}')

    trans_probs_filename =  f'{ddir}/trans_probs.txt'
    output_probs_filename = f'{ddir}/output_probs.txt'

    in_tags_filename = f'{ddir}/twitter_tags.txt'
    viterbi_predictions_filename = f'{ddir}/viterbi_predictions.txt'
    viterbi_predict(in_tags_filename, trans_probs_filename, output_probs_filename, in_test_filename,
                    viterbi_predictions_filename)
    correct, total, acc = evaluate(viterbi_predictions_filename, in_ans_filename)
    print(f'Viterbi prediction accuracy:   {correct}/{total} = {acc}')

    # trans_probs_filename2 =  f'{ddir}/trans_probs2.txt'
    # output_probs_filename2 = f'{ddir}/output_probs2.txt'

    # viterbi_predictions_filename2 = f'{ddir}/viterbi_predictions2.txt'
    # viterbi_predict2(in_tags_filename, trans_probs_filename2, output_probs_filename2, in_test_filename,
    #                  viterbi_predictions_filename2)
    # correct, total, acc = evaluate(viterbi_predictions_filename2, in_ans_filename)
    # print(f'Viterbi2 prediction accuracy:  {correct}/{total} = {acc}')
    


if __name__ == '__main__':
    run()
