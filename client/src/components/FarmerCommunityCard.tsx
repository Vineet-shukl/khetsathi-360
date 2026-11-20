import React, { useState } from 'react';
import type { FPOCluster } from '../types/contracts';

interface FarmerCommunityCardProps {
  locationName: string;
  isHi: boolean;
  cropName: string;
}

const REGIONAL_FPOS: FPOCluster[] = [
  {
    name: 'गाज़ीपुर किसान समृद्धि कृषक उत्पादक कंपनी',
    district: 'Ghazipur',
    state: 'Uttar Pradesh',
    commodities: ['गेहूं (Wheat)', 'धान (Paddy)', 'सब्जियां (Vegetables)'],
    contact_person: 'राकेश कुशवाहा (निदेशक)',
    phone: '+91 94501 23456',
    address: 'मंडी परिसर, जंगीपुर रोड, गाज़ीपुर',
    verified: true,
  },
  {
    name: 'काशी एग्रो फार्मर प्रोड्यूसर कंपनी लिमिटेड',
    district: 'Varanasi',
    state: 'Uttar Pradesh',
    commodities: ['जैविक बासमती (Organic Basmati)', 'सरसों (Mustard)'],
    contact_person: 'अमित कुमार सिंह (मुख्य कार्यकारी)',
    phone: '+91 98390 87654',
    address: 'राजातालाब, वाराणसी',
    verified: true,
  },
  {
    name: 'करनाल प्रगतिशील किसान उत्पादक समूह',
    district: 'Karnal',
    state: 'Haryana',
    commodities: ['गेहूं (Wheat HD-2967/3086)', 'बासमती 1121/1509'],
    contact_person: 'गुरप्रीत सिंह संधू',
    phone: '+91 98120 11223',
    address: 'जीटी रोड, नजदीक नई अनाज मंडी, करनाल',
    verified: true,
  },
];

export const FarmerCommunityCard: React.FC<FarmerCommunityCardProps> = ({
  locationName,
  isHi,
  cropName,
}) => {
  const [farmerPostText, setFarmerPostText] = useState('');
  const [posts, setPosts] = useState<
    { author: string; village: string; time: string; text: string; likes: number }[]
  >([
    {
      author: 'राजेश यादव',
      village: 'मुहम्मदाबाद, गाज़ीपुर',
      time: '2 घंटे पहले',
      text: 'इस बार डीएपी की जगह वर्मीकम्पोस्ट और तरल बायो-एनपीके डाला था, गेहूं की कल्ले फूटने (tillering) की गति रासायनिक खाद से भी बेहतर है!',
      likes: 14,
    },
    {
      author: 'सतपाल मलिक',
      village: 'घरौंडा, करनाल',
      time: '5 घंटे पहले',
      text: 'मौसम चेतावनी बिल्कुल सही थी, कल रात हल्की बारिश हुई। यूरिया छिड़काव टालने से भारी बचत हुई!',
      likes: 21,
    },
  ]);

  const handleShareOnWhatsAppGroup = () => {
    const text = isHi
      ? `🌾 *KhetSathi 360 — स्थानीय किसान समुदाय व मंडी लिंकेज*\n\nस्थान: ${locationName}\nफसल: ${cropName}\n\nमैं अपने क्षेत्र के किसान भाइयों और एफपीओ समूह से जुड़ना चाहता हूँ। कृपया समूह में जोड़ें।\n\nसत्यापित पोर्टल: https://khetsathi-360.onrender.com`
      : `🌾 *KhetSathi 360 — Local Farmer Community & Mandi Linkage*\n\nLocation: ${locationName}\nCrop: ${cropName}\n\nI want to connect with local farmers and regional FPO cluster in our block.\n\nVerified Portal: https://khetsathi-360.onrender.com`;
    window.open(`https://api.whatsapp.com/send?text=${encodeURIComponent(text)}`, '_blank');
  };

  const handlePostSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!farmerPostText.trim()) return;
    setPosts([
      {
        author: isHi ? 'आप (प्रगतिशील किसान)' : 'You (Farmer)',
        village: locationName.split(',')[0] || 'मेरा गाँव',
        time: isHi ? 'अभी-अभी' : 'Just now',
        text: farmerPostText,
        likes: 1,
      },
      ...posts,
    ]);
    setFarmerPostText('');
  };

  return (
    <div className="space-y-6">
      {/* Header Card */}
      <div className="fable-card p-6 rounded-3xl bg-gradient-to-br from-white to-[#f4efe6] space-y-2">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div>
            <span className="text-[11px] font-black uppercase tracking-wider text-[#143826] bg-emerald-100 px-2.5 py-1 rounded-full border border-emerald-300">
              {isHi ? '🤝 किसान-से-किसान नेटवर्क' : '🤝 Peer-to-Peer Farmer Network'}
            </span>
            <h2 className="text-xl sm:text-2xl font-black text-[#143826] font-serif-fable mt-1">
              {isHi ? 'स्थानीय किसान समुदाय व एफपीओ संपर्क' : 'Connect with Local Farmers & FPO Hubs'}
            </h2>
          </div>

          <button
            type="button"
            onClick={handleShareOnWhatsAppGroup}
            className="min-h-[44px] px-5 py-2.5 bg-emerald-700 hover:bg-emerald-800 text-white font-bold text-xs sm:text-sm rounded-xl shadow-md transition flex items-center justify-center gap-2 cursor-pointer self-start sm:self-auto"
          >
            <span>📲</span>
            <span>{isHi ? 'किसान व्हाट्सएप ग्रुप में जुड़ें' : 'Join Local WhatsApp Group'}</span>
          </button>
        </div>

        <p className="text-xs sm:text-sm text-[#5f6b64] leading-relaxed">
          {isHi
            ? `स्थान: 📍 ${locationName}। अपने ब्लॉक व जिले के साथी किसानों से जुड़ें, अनुभव साझा करें और सरकारी सहायता प्राप्त एफपीओ से सीधे जुड़ें।`
            : `Location: 📍 ${locationName}. Connect with neighboring farmers, share field observations, and access verified regional FPO aggregation hubs.`}
        </p>
      </div>

      {/* Emergency & KVK Helpline Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {/* National Kisan Call Center */}
        <div className="fable-card p-5 rounded-2xl flex items-center justify-between gap-3 border-l-4 border-l-emerald-600">
          <div className="flex items-center gap-3">
            <div className="w-12 h-12 rounded-2xl bg-emerald-100 flex items-center justify-center text-2xl shrink-0">
              📞
            </div>
            <div>
              <span className="text-xs font-bold text-slate-500 block">
                {isHi ? 'राष्ट्रीय किसान कॉल सेंटर (निःशुल्क)' : 'National Kisan Call Center (Toll-Free)'}
              </span>
              <span className="text-base font-black text-[#143826]">
                1800-180-1551
              </span>
              <p className="text-[11px] text-slate-500">
                {isHi ? 'सुबह 6:00 से रात 10:00 तक सभी 22 भाषाओं में' : '6:00 AM – 10:00 PM in 22 regional languages'}
              </p>
            </div>
          </div>
          <a
            href="tel:18001801551"
            className="min-h-[44px] px-4 py-2 bg-emerald-700 hover:bg-emerald-800 text-white font-bold text-xs rounded-xl shadow-sm transition flex items-center gap-1.5 shrink-0"
          >
            <span>📞</span> <span>{isHi ? 'कॉल करें' : 'Call'}</span>
          </a>
        </div>

        {/* Local KVK Scientists */}
        <div className="fable-card p-5 rounded-2xl flex items-center justify-between gap-3 border-l-4 border-l-[#c96442]">
          <div className="flex items-center gap-3">
            <div className="w-12 h-12 rounded-2xl bg-amber-100 flex items-center justify-center text-2xl shrink-0">
              🔬
            </div>
            <div>
              <span className="text-xs font-bold text-slate-500 block">
                {isHi ? 'कृषि विज्ञान केंद्र (KVK) वैज्ञानिक हेल्पलाइन' : 'Krishi Vigyan Kendra (KVK) Helpline'}
              </span>
              <span className="text-sm font-bold text-[#143826]">
                {locationName.split(',')[0]} KVK नोडल अधिकारी
              </span>
              <p className="text-[11px] text-slate-500">
                {isHi ? 'बीज, कीट नियंत्रण व मिट्टी सुधार परामर्श' : 'Seed quality, pest defense & soil consultation'}
              </p>
            </div>
          </div>
          <button
            type="button"
            onClick={() => alert(isHi ? `📍 आपके जिले (${locationName.split(',')[0]}) का KVK केंद्र सक्रिय है। संपर्क समय: सुबह 9 से शाम 5 बजे।` : `Active KVK Center for ${locationName.split(',')[0]}. Hours: 9 AM - 5 PM.`)}
            className="min-h-[44px] px-4 py-2 bg-[#c96442] hover:bg-[#b85836] text-white font-bold text-xs rounded-xl shadow-sm transition flex items-center gap-1.5 shrink-0 cursor-pointer"
          >
            <span>ℹ️</span> <span>{isHi ? 'विवरण' : 'Details'}</span>
          </button>
        </div>
      </div>

      {/* Verified Regional FPOs Grid */}
      <div className="fable-card p-6 rounded-3xl space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-[#e6dfd3] pb-3">
          <div>
            <h3 className="text-base font-bold text-[#143826] flex items-center gap-2">
              <span>🏪</span>
              <span>{isHi ? 'नजदीकी सत्यापित कृषक उत्पादक संगठन (FPO Clusters)' : 'Verified Nearby FPO Aggregation Clusters'}</span>
            </h3>
            <p className="text-xs text-[#5f6b64]">
              {isHi
                ? 'सामूहिक खाद खरीद, उन्नत बीज आपूर्ति एवं खेत से सीधी फसल खरीद हेतु पंजीकृत समूह'
                : 'Bulk input procurement, certified seed access, and direct farmgate purchase hubs'}
            </p>
          </div>
          <span className="text-xs font-black text-emerald-800 bg-emerald-100 px-3 py-1 rounded-full border border-emerald-300 self-start sm:self-auto">
            SFAC & NABARD
          </span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
          {REGIONAL_FPOS.map((fpo, idx) => (
            <div
              key={idx}
              className="p-4 rounded-2xl bg-[#faf8f5] border border-[#e6dfd3] space-y-2 flex flex-col justify-between"
            >
              <div className="space-y-1">
                <div className="flex items-start justify-between gap-1">
                  <h4 className="text-xs sm:text-sm font-bold text-[#143826]">
                    {fpo.name}
                  </h4>
                  <span className="text-[10px] font-extrabold text-emerald-700 bg-emerald-100 px-1.5 py-0.5 rounded shrink-0">
                    ✓ Verified
                  </span>
                </div>
                <p className="text-[11px] text-[#5f6b64]">
                  📍 {fpo.address}
                </p>
                <div className="flex flex-wrap gap-1 pt-1">
                  {fpo.commodities.map((c, i) => (
                    <span
                      key={i}
                      className="text-[9px] font-semibold bg-white border border-[#e6dfd3] px-1.5 py-0.5 rounded text-slate-700"
                    >
                      {c}
                    </span>
                  ))}
                </div>
              </div>

              <div className="pt-2 border-t border-[#e6dfd3] flex items-center justify-between text-xs">
                <span className="text-[11px] text-[#5f6b64] font-medium">
                  {fpo.contact_person}
                </span>
                <a
                  href={`tel:${fpo.phone}`}
                  className="font-bold text-emerald-800 hover:text-emerald-950 flex items-center gap-1"
                >
                  <span>📞</span> <span>{fpo.phone}</span>
                </a>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Community Experience Share Board */}
      <div className="fable-card p-6 rounded-3xl space-y-4">
        <div className="border-b border-[#e6dfd3] pb-3">
          <h3 className="text-base font-bold text-[#143826] flex items-center gap-2">
            <span>💬</span>
            <span>{isHi ? 'किसान अनुभव व स्थानीय चर्चा मंच' : 'Farmer Experience & Community Discussion'}</span>
          </h3>
          <p className="text-xs text-[#5f6b64]">
            {isHi ? 'अपने खेत के अनुभव साझा करें या सलाह प्राप्त करें' : 'Post field observations or ask questions to local farmers'}
          </p>
        </div>

        {/* Input box */}
        <form onSubmit={handlePostSubmit} className="space-y-2">
          <textarea
            value={farmerPostText}
            onChange={(e) => setFarmerPostText(e.target.value)}
            rows={2}
            placeholder={
              isHi
                ? 'अपने खेत का अनुभव, खाद की बचत या फसल की स्थिति यहाँ लिखें...'
                : 'Write your field observation, fertilizer savings or question here...'
            }
            className="w-full p-3 rounded-xl border border-slate-300 text-xs sm:text-sm bg-white focus:outline-none focus:ring-2 focus:ring-emerald-600 resize-none"
          />
          <div className="flex justify-end">
            <button
              type="submit"
              className="min-h-[44px] px-5 py-2 bg-[#143826] hover:bg-[#1f4f37] text-white font-bold text-xs rounded-xl shadow-sm transition flex items-center gap-1.5 cursor-pointer"
            >
              <span>📢</span>
              <span>{isHi ? 'समुदाय में साझा करें' : 'Post to Community'}</span>
            </button>
          </div>
        </form>

        {/* Posts list */}
        <div className="space-y-3 pt-2">
          {posts.map((post, idx) => (
            <div
              key={idx}
              className="p-3.5 rounded-2xl bg-[#faf8f5] border border-[#e6dfd3] space-y-1.5"
            >
              <div className="flex items-center justify-between text-xs">
                <div className="flex items-center gap-2">
                  <span className="w-7 h-7 rounded-full bg-emerald-100 flex items-center justify-center font-bold text-[#143826] text-xs">
                    {post.author[0]}
                  </span>
                  <div>
                    <span className="font-bold text-[#143826] block">
                      {post.author}
                    </span>
                    <span className="text-[10px] text-slate-500">
                      📍 {post.village} · {post.time}
                    </span>
                  </div>
                </div>

                <button
                  type="button"
                  onClick={() => {
                    const newPosts = [...posts];
                    newPosts[idx].likes += 1;
                    setPosts(newPosts);
                  }}
                  className="px-2 py-1 rounded-lg bg-white border border-[#e6dfd3] hover:border-emerald-500 text-[11px] font-bold text-slate-700 flex items-center gap-1 transition cursor-pointer"
                >
                  <span>👍</span> <span>{post.likes}</span>
                </button>
              </div>

              <p className="text-xs text-slate-700 leading-relaxed pl-9">
                {post.text}
              </p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
