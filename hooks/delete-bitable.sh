#!/bin/bash
# Bot Quality Monitor - 删除飞书多维表格
# 运行此脚本会删除 Bot 创建的多维表格（不可恢复，请谨慎！）

echo "⚠️  此操作将删除飞书上的 Bot Quality Monitor 多维表格"
echo "   删除后数据无法恢复，请谨慎操作！"
echo ""
echo "请确认你要删除的是哪个多维表格："
echo ""
echo "1. 我知道 App Token，直接输入删除"
echo "2. 不知道 App Token，让 Bot 帮忙查"
echo "3. 取消，不删除"
echo ""
read -p "请选择 (1/2/3): " choice

case $choice in
    1)
        echo ""
        read -p "请输入 App Token (形如 Xw4Tb5C8KagMiQswkdacNfVPn8e): " app_token
        if [ -z "$app_token" ]; then
            echo "❌ 未输入 App Token，取消操作"
            exit 1
        fi
        echo ""
        echo "❓ 你确定要删除 App Token 为 $app_token 的多维表格吗？"
        read -p "输入 'YES' 确认删除: " confirm
        if [ "$confirm" = "YES" ]; then
            echo "🗑️  正在删除多维表格..."
            # 这里需要调用飞书 API 删除应用，实际由 Bot 执行
            echo ""
            echo "请对你的 Bot 说："
            echo "   删除多维表格 $app_token"
            echo ""
            echo "Bot 会帮你完成删除操作。"
        else
            echo "❌ 取消操作"
        fi
        ;;
    2)
        echo ""
        echo "请对你的 Bot 说："
        echo "   查看质量监控配置"
        echo ""
        echo "Bot 会告诉你当前的 App Token，然后你可以运行："
        echo "   ./hooks/delete-bitable.sh"
        echo "来删除它。"
        ;;
    3)
        echo "❌ 已取消"
        ;;
    *)
        echo "❌ 无效选择，请输入 1、2 或 3"
        ;;
esac

echo ""
echo "💡 提示：如果不想用脚本，也可以直接去飞书操作："
echo "   飞书 → 云空间 → 多维表格 → 找到 Bot Quality Monitor → 删除"