planemo tool_init --id 'pm_muairss_write' \
                  --name 'Generate muon structures (pm-muairss)' \
                  --example_command 'pm-muairss -t w Si.cell Si-muairss-castep.yaml; zip -r si-muon-airss-out.zip si-muon-airss-out' \
                  --example_input Si.cell \
                  --example_input Si-muairss-castep.yaml \
                  --example_output si-muon-airss-out.zip \
                  --test_case \
                  --cite_url 'https://github.com/muon-spectroscopy-computational-project/pymuon-suite/' \
                  --help_from_command 'pm-muairss'
                  #--requirement pymuon-suite@0.1.0 \

planemo shed_init --category 'Computational chemistry, Molecular Dynamics' \
                  --description 'Generate muon structures (pm-muairss)' \
                  --long_description 'TODO' \
                  --homepage_url 'https://github.com/muon-spectroscopy-computational-project/muon-galaxy-tools' \
                  --remote_repository_url 'https://github.com/muon-spectroscopy-computational-project/muon-galaxy-tools/main/pm_muairss_write' \
                  --owner 'elichad'
