import os
import cloudpickle

def deserialize_model(parts_dir,output_dir):

    merged_data = b""
    part_files = [file for file in os.listdir(parts_dir) if file.endswith('.pkl')]
    num_parts = len(part_files)

    print(f"Rebuilding file from {num_parts} parts...\n")
    for i in range(num_parts):
        print(f"Merging file {i+1} of {num_parts}... ", end="")
        part_files_path = os.path.join(parts_dir, f"part_{i}.pkl")
        with open(part_files_path,'rb') as f:
            merged_data += f.read()
        print("OK")

    os.makedirs(output_dir, exist_ok=True)
    print("\nDeserializing merged model... ", end="")
    deserialized_model = cloudpickle.loads(merged_data)
    print("OK\n")

    return deserialized_model

if __name__ == "__main__":

    parts_dir = 'output'
    output_dir = 'rebuild'

    clf = deserialize_model('output','rebuild')

    print(f"Saving deserialized model in {output_dir}...\n")
    with open(f"{output_dir}/rebuilt_model.pkl", "wb") as outfile:
        cloudpickle.dump(clf,outfile)

    print("### REBUILD COMPLETE! ###\n")