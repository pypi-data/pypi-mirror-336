from metabomix import MetaboMix

def main():
    settings_path: str = "/lustre/BIF/nobackup/hendr218/metabomix/Example/Example_recipe.json"
    test_workflow = metabomix.MetaboMix(settings_path)

if __name__ == "__main__":
    main()