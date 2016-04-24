from __future__ import division
import io


def load_set(set_file):
    out = set()
    with io.open(set_file, errors="ignore") as ifile:
        for line in ifile:
            out.add(line.rstrip())
    return out


def find_common(gen_file, target_file, common_output=None):
    target_passwords = load_set(target_file)
    print("[find_in_file] Loaded %d from password list" % len(target_passwords))
    return find_common_preload(gen_file, target_passwords, common_output)


def find_common_preload(gen_file, target_passwords, common_output=None):
    generated_passwords = load_set(gen_file)

    print("[find_in_file] Loaded %d generated passwords" % len(generated_passwords))

    shared_passwords = set()
    for potential in generated_passwords:
        if potential in target_passwords:
            shared_passwords.add(potential)

    if common_output is not None:
        with open(common_output, "w") as outfile:
            outfile.write("\n".join(shared_passwords))

    return len(shared_passwords), len(shared_passwords)/len(generated_passwords), shared_passwords
