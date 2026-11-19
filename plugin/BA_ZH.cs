using System;
using System.Collections;
using System.Collections.Generic;
using System.Reflection;
using BepInEx;
using TMPro;
using UnityEngine;

namespace BA_ZH
{
    // The game swaps a TMP component's font only inside Txt.Write(text_id).
    // Text assigned by code (TMP_Dropdown options / labels, etc.) keeps the default
    // "cuyabra" font, which has zero CJK glyphs -> every Chinese character shows as a box.
    // Putting the game's own zh_white / zh_black into TMP's global fallback list fixes
    // all of them at once, in every language, without touching any game file.
    [BepInPlugin(GUID, "Bondage Arena Chinese Font Fix", "1.1.0")]
    public class Plugin : BaseUnityPlugin
    {
        public const string GUID = "com.a404670637ch.ba_zh_font";

        private static readonly string[] CJK_FONTS = new string[] { "zh_white", "zh_black" };
        private static readonly string[] FALLBACK_FIELDS = new string[] { "m_fallbackFontAssetTable", "m_fallbackFontAssets" };
        private bool _done;

        private void Awake()
        {
            Logger.LogInfo("BA_ZH: loaded");
            StartCoroutine(Watch());
        }

        private IEnumerator Watch()
        {
            while (true)
            {
                yield return new WaitForSeconds(1.5f);
                try
                {
                    if (!_done && TryApply())
                    {
                        _done = true;
                        Logger.LogInfo("BA_ZH: CJK fallback injected");
                    }
                }
                catch (Exception e)
                {
                    Logger.LogWarning("BA_ZH: " + e.Message);
                }
            }
        }

        private bool TryApply()
        {
            List<TMP_FontAsset> fallbacks = GetFallbackList();
            if (fallbacks == null) return false;

            TMP_FontAsset[] fonts = Resources.FindObjectsOfTypeAll<TMP_FontAsset>();
            if (fonts == null || fonts.Length == 0) return false;

            bool changed = false;
            for (int k = 0; k < CJK_FONTS.Length; k++)
            {
                for (int i = 0; i < fonts.Length; i++)
                {
                    TMP_FontAsset f = fonts[i];
                    if (f != null && f.name == CJK_FONTS[k] && !fallbacks.Contains(f))
                    {
                        fallbacks.Add(f);
                        changed = true;
                        break;
                    }
                }
            }
            if (!changed) return false;

            // texts rendered before the injection keep their cached glyphs
            TMP_Text[] texts = Resources.FindObjectsOfTypeAll<TMP_Text>();
            for (int i = 0; i < texts.Length; i++)
            {
                if (texts[i] != null) texts[i].SetAllDirty();
            }
            return true;
        }

        private static List<TMP_FontAsset> GetFallbackList()
        {
            try
            {
                TMP_Settings settings = TMP_Settings.instance;
                if (settings == null) return null;

                Type t = typeof(TMP_Settings);
                PropertyInfo prop = t.GetProperty("fallbackFontAssets", BindingFlags.Public | BindingFlags.Static);
                if (prop != null)
                {
                    List<TMP_FontAsset> list = prop.GetValue(null, null) as List<TMP_FontAsset>;
                    if (list != null) return list;
                }
                for (int i = 0; i < FALLBACK_FIELDS.Length; i++)
                {
                    FieldInfo field = t.GetField(FALLBACK_FIELDS[i], BindingFlags.NonPublic | BindingFlags.Instance);
                    if (field == null) continue;
                    List<TMP_FontAsset> list = field.GetValue(settings) as List<TMP_FontAsset>;
                    if (list == null)
                    {
                        list = new List<TMP_FontAsset>();
                        field.SetValue(settings, list);
                    }
                    return list;
                }
            }
            catch (Exception) { }
            return null;
        }
    }
}
