planemo tool_init --force \
                  --id 'pm-muairss_write' \
                  --name 'Generate muon structures (pm-muairss)' \
                  --example_command 'pm-muairss -t w Si.cell Si-muairss-castep.yaml; zip -r si-muon-airss-out.zip si-muon-airss-out' \
                  --example_input Si.cell \
                  --example_input Si-muairss-castep.yaml \
                  --example_output si-muon-airss-out.zip \
                  --test_case \
                  --cite_url 'https://github.com/muon-spectroscopy-computational-project/pymuon-suite/' \
                  --help_from_command 'pm-muairss'
                  #--requirement pymuon-suite@0.1.0 \
