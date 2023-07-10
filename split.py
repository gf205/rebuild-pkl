import os
import cloudpickle

def serialize_model(original_model_path, output_dir):

    print(f"Loading the model from {original_model_path}...", end='')
    with open(original_model_path,'rb') as f:
        # load the model from the original .pkl
        original_model = cloudpickle.load(f)
    print(f"OK\n")

    # serialize the model to accomodate for multi-part splitting
    print(f"Serializing the model...",end='')
    serialized_model = cloudpickle.dumps(original_model)
    print(f"OK\n")

    # get the number of parts required to save the entire file given a certain {part_size}
    part_size = 10 * 1024 * 1024        # 10MB
    num_parts = (len(serialized_model) + part_size - 1) // part_size

    # create the output directory if it doesn't already exist
    os.makedirs(output_dir, exist_ok=True)

    print(f"Dumping {num_parts} parts into {output_dir}...")
    for i in range(num_parts):
        print(f"Dumping part {i} of {num_parts}...",end='')
        part_start = i * part_size
        part_end = min((i + 1) * part_size, len(serialized_model))
        part_data = serialized_model[part_start:part_end]

        part_file_path = os.path.join(output_dir, f"part_{i}.pkl")
        with open(part_file_path, 'wb') as f:
            f.write(part_data)
            print(' OK')

    print(f"\n### Pickle split complete! Files saved in '{output_dir}' ###")


if __name__ == "__main__":

    original_model_path = 'test/testfile.pkl'
    output_dir = 'output'

    serialize_model(original_model_path,output_dir)