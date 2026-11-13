def calc_iou(c1: tuple, c2: tuple) -> float:
    intersection = min(c1[1], c2[1]) - max(c1[0], c2[0])
    if intersection < 0:
        return 0.0
    union = (c1[1] - c1[0]) + (c2[1] - c2[0]) - intersection
    return intersection / union if union > 0 else 0.0


def calc_recall_k(retrieved_source, ground_truth, k):
    retrieved_chunks = retrieved_source['retrieved_chunks'][:k]

    for i, chunk in enumerate(retrieved_chunks, start=1):
        if chunk['path'] == ground_truth['sources'][0]['path']:
            c1 = (chunk['first_char'], chunk['last_char'])
            c2 = (ground_truth['sources'][0]['first_char'], ground_truth['sources'][0]['last_char'])

            if calc_iou(c1, c2) >= 0.05:
                return i

    return -1


import json

with open('retrieved_data.json', 'r') as f:
    retrieved_data = json.load(f)

with open('ground_truth.json', 'r') as f:
    ground_truth = json.load(f)


print('Evaluation Results')
print('==================')
print(f'Question evaluated: {len(ground_truth)}')
for k in [1, 3, 5]:
    success = 0
    for i, minimal_source in enumerate(retrieved_data):
        if minimal_source['question'] == ground_truth[i]['question']:
            top_k = calc_recall_k(minimal_source, ground_truth[i], k=k)

            if top_k > 0:
                success += 1


    recall_at_k = success * 100 / len(ground_truth)
    print(f'Recall@{k}: {success}/{len(ground_truth)} ({recall_at_k:.2f})%')
