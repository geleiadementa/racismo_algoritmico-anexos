set export := true

#-------------------------------------------------------------------------------
raw_images := 
labels := 
#-------------------------------------------------------------------------------
dataset_dir := absolute_path("datasets")
dataset_base := join(dataset_dir, "base.csv")
dataset_sample := join(dataset_dir, "sample.csv")
#-------------------------------------------------------------------------------
n_amostras := "100"
resultados := "resultados.csv"
output_dir := absolute_path("output")
#-------------------------------------------------------------------------------
seed := "62733" # gerado por: od -N2 -vAn -d /dev/random
hash_dir := absolute_path("hash")
#-------------------------------------------------------------------------------
_scripts_dir := absolute_path("prepare_data")
make_dataset_base := join(_scripts_dir, "make_base.py")
make_dataset_groups := join(_scripts_dir, "make_samples.py")
models := "process/deepface.py"
#-------------------------------------------------------------------------------
_conda := 
python_env := "racismo-algoritmico"
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

make_datasets_samples:
    @echo "gerando o dataset com amostragens:"
    {{ python_bin }} {{ absolute_path(make_dataset_groups) }}
    @echo "calculando o hash:"
    @echo {{sha256_file(dataset_sample)}} {{file_name(dataset_sample)}} | tee {{hash_dir}}/{{file_stem(dataset_sample)}}.txt
