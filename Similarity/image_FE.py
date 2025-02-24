from common_imports import *

def image_FE(root_path):
    feature_extractor = ViTFeatureExtractor.from_pretrained('google/vit-base-patch16-224')
    model = ViTModel.from_pretrained('google/vit-base-patch16-224')

    # ================================================================
    features_dict = {}
    img_data = sorted(os.listdir(root_path), key=lambda x: int(x.split('-')[0]))

    for img_name in tqdm(img_data):
        try:
            image_path = os.path.join(root_path, img_name)
            image = Image.open(image_path).convert("RGB")
            
            inputs = feature_extractor(images=image, return_tensors="pt")
            
            # feature extraction
            with torch.no_grad():
                outputs = model(**inputs)
                feature = outputs.last_hidden_state
                feature = feature[0].mean(dim=0)
            
            # feature shape:(1, 768)
            features_dict[img_name] = feature.unsqueeze(0).numpy()
            
        except Exception as e:
            print(f"Error processing {img_name}: {e}")
            continue

    with open(f'./data/img_data/IMG_vit_features.pkl', 'wb') as f:
        pickle.dump(features_dict, f)