set export := true

#-------------------------------------------------------------------------------
raw_images := 
labels := 
identity_meta := 
#-------------------------------------------------------------------------------
dataset_dir := absolute_path("datasets")
dataset_base := join(dataset_dir, "base.csv")
dataset_sample := join(dataset_dir, "sample.csv")
dataset_resultado := join(dataset_dir, "deepface_resultado.csv")
#-------------------------------------------------------------------------------
n_amostras := "10"
n_imgs := "5"
resultados := "resultados.csv"
output_dir := absolute_path("output")
output_deepface := join(output_dir, "deepface.json")
#-------------------------------------------------------------------------------
seed := "62733" # gerado por: od -N2 -vAn -d /dev/random
hash_dir := absolute_path("hash")
#-------------------------------------------------------------------------------
_scripts_dir := absolute_path("prepare_data")
make_dataset_base := join(_scripts_dir, "make_base.py")
make_dataset_groups := join(_scripts_dir, "make_samples.py")
make_output_deepface := join(_scripts_dir, "run_deepface.py")
#-------------------------------------------------------------------------------
analyze_path := absolute_path("analyze")
gen_cards := join(analyze_path, 'result_cards.py')
#-------------------------------------------------------------------------------
_conda := "/home/lincoln/.miniconda"
python_env := "raa"
python_bin := _conda / "envs" / python_env / "bin/python"
conda_packages := "conda-package-list.txt"
#-------------------------------------------------------------------------------
#..................................logging......................................
TF_CPP_MIN_LOG_LEVEL := "3"
#-------------------------------------------------------------------------------

default:
    @just --list

install_deps:
    #!/usr/bin/env sh
    if [ -x {{ _conda }}/bin/conda ]; then
        {{ _conda }}/bin/activate
        conda create -n {{ python_env }} --file {{ conda_packages }}
        pip install polars tf-explain
    else
        echo "instale o conda ou o miniconda: https://docs.conda.io/en/latest/miniconda.html"
    fi

create_dirs:
    @echo "criando diretórios:"
    mkdir -p {{ dataset_dir }}
    mkdir -p {{ hash_dir }}
    mkdir -p {{ output_dir }}/notebooks
    mkdir -p {{ output_dir }}/images
    @echo "--------------------------------------------------------------------------------"

make_dataset_base:
    @just create_dirs    
    @echo "construindo o dataset-base:"
    {{ python_bin }} {{ absolute_path(make_dataset_base) }}
    @echo "calculando o hash:"
    @echo {{sha256_file(dataset_base)}} {{file_name(dataset_base)}} | tee {{hash_dir}}/{{file_stem(dataset_base)}}.txt

make_dataset_sample:
    @echo "gerando o dataset com amostragens:"
    {{ python_bin }} {{ absolute_path(make_dataset_groups) }}
    @echo "calculando o hash:"
    @echo {{sha256_file(dataset_sample)}} {{file_name(dataset_sample)}} | tee {{hash_dir}}/{{file_stem(dataset_sample)}}.txt

make_output_deepface:
    @echo "aplicando o deepface nas amostras:"
    {{ python_bin }} {{ absolute_path(make_output_deepface) }}
    @echo "calculando o hash:"
    @echo {{ sha256_file(dataset_resultado) }} {{ file_name(dataset_resultado) }} | tee {{hash_dir}}/{{ file_stem(dataset_resultado)}}.txt
    @echo {{ sha256_file(output_deepface) }} {{ file_name(output_deepface) }} | tee {{hash_dir}}/{{ file_stem(output_deepface)}}.txt

gen_image_cards:
    @echo "gerando gráficos de cada imagem"
    {{ python_bin }} {{ absolute_path(gen_cards) }}

run:
    @just create_dirs
    @just make_dataset_base
    @just make_datasets_samples
    @just make_output_deepface
    @just gen_image_cards