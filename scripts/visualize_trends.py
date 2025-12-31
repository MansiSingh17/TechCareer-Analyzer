#!/usr/bin/env python3
"""
Create professional visualizations for tech career trends
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from backend.utils.db import get_db
from backend.models.job import Job
from collections import Counter

# Set professional style
sns.set_style("whitegrid")
sns.set_palette("husl")
plt.rcParams['figure.figsize'] = (14, 8)
plt.rcParams['font.size'] = 11

def visualize_all_trends(output_dir: str = "./visualizations"):
    """Create all visualizations"""
    
    os.makedirs(output_dir, exist_ok=True)
    
    print("\n" + "="*70)
    print("🎨 CREATING VISUALIZATIONS")
    print("="*70)
    
    with get_db() as db:
        jobs = db.query(Job).all()
        
        if not jobs:
            print("❌ No job data found in database!")
            print("\nRun one of these first:")
            print("  python scripts/init_db.py --seed")
            print("  python scripts/collect_jobs.py --save-db")
            return
        
        print(f"📊 Using {len(jobs)} jobs from database\n")
        
        # 1. Top Skills Bar Chart
        print("1️⃣  Creating Top Skills chart...")
        create_top_skills_chart(jobs, output_dir)
        
        # 2. Salary Distribution
        print("2️⃣  Creating Salary Distribution chart...")
        create_salary_distribution(jobs, output_dir)
        
        # 3. Experience vs Skills
        print("3️⃣  Creating Experience Analysis charts...")
        create_experience_analysis(jobs, output_dir)
        
        # 4. Location Analysis
        print("4️⃣  Creating Location Analysis chart...")
        create_location_chart(jobs, output_dir)
        
        # 5. Tech Stack Heatmap
        print("5️⃣  Creating Tech Stack Heatmap...")
        create_tech_stack_heatmap(jobs, output_dir)
        
        print("\n" + "="*70)
        print("✅ ALL VISUALIZATIONS CREATED!")
        print("="*70)
        print(f"\n📁 Saved to: {output_dir}/")
        print("   • top_skills.png")
        print("   • salary_distribution.png")
        print("   • experience_analysis.png")
        print("   • top_locations.png")
        print("   • tech_stack_heatmap.png")
        print("\n💡 Open these files to view your charts!")
        print("="*70)

def create_top_skills_chart(jobs, output_dir):
    """Create horizontal bar chart of top skills"""
    all_skills = []
    for job in jobs:
        if job.required_skills:
            all_skills.extend(job.required_skills)
    
    skill_counts = Counter(all_skills)
    top_skills = skill_counts.most_common(20)
    
    if not top_skills:
        print("   ⚠️  No skills data found")
        return
    
    skills, counts = zip(*top_skills)
    
    plt.figure(figsize=(14, 10))
    colors = sns.color_palette("viridis", len(skills))
    plt.barh(range(len(skills)), counts, color=colors)
    plt.yticks(range(len(skills)), skills, fontsize=12)
    plt.xlabel('Number of Job Postings', fontsize=13, fontweight='bold')
    plt.title('Top 20 Most In-Demand Tech Skills', fontsize=16, fontweight='bold', pad=20)
    plt.gca().invert_yaxis()
    
    # Add value labels
    for i, (skill, count) in enumerate(zip(skills, counts)):
        plt.text(count + 0.5, i, str(count), va='center', fontsize=10)
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/top_skills.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"   ✅ Saved: top_skills.png")

def create_salary_distribution(jobs, output_dir):
    """Create boxplot of salary distribution by role"""
    salary_data = []
    for job in jobs:
        if job.salary and job.salary > 0:
            salary_data.append({
                'role': job.title,
                'salary': job.salary
            })
    
    if not salary_data:
        print("   ⚠️  No salary data found")
        return
    
    df_salary = pd.DataFrame(salary_data)
    
    # Get top roles by count
    top_roles = df_salary['role'].value_counts().head(8).index
    df_top_roles = df_salary[df_salary['role'].isin(top_roles)]
    
    plt.figure(figsize=(16, 10))
    
    # Create boxplot
    box_plot = sns.boxplot(
        data=df_top_roles, 
        y='role', 
        x='salary',
        palette='Set2',
        width=0.6
    )
    
    plt.xlabel('Annual Salary (USD)', fontsize=13, fontweight='bold')
    plt.ylabel('Job Role', fontsize=13, fontweight='bold')
    plt.title('Salary Distribution by Role', fontsize=16, fontweight='bold', pad=20)
    
    # Format x-axis
    plt.ticklabel_format(style='plain', axis='x')
    ax = plt.gca()
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1000:.0f}K'))
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/salary_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"   ✅ Saved: salary_distribution.png")

def create_experience_analysis(jobs, output_dir):
    """Create scatter plots for experience analysis"""
    exp_data = []
    for job in jobs:
        exp_data.append({
            'experience': job.experience_required,
            'skill_count': len(job.required_skills) if job.required_skills else 0,
            'salary': job.salary if job.salary else 0
        })
    
    df_exp = pd.DataFrame(exp_data)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 7))
    
    # Experience vs Skill Count
    ax1.scatter(df_exp['experience'], df_exp['skill_count'], 
               alpha=0.6, color='coral', s=80, edgecolors='darkred', linewidth=0.5)
    ax1.set_xlabel('Years of Experience Required', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Number of Required Skills', fontsize=12, fontweight='bold')
    ax1.set_title('Skills Requirements vs Experience Level', fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    
    # Add trend line
    z = np.polyfit(df_exp['experience'], df_exp['skill_count'], 1)
    p = np.poly1d(z)
    ax1.plot(df_exp['experience'], p(df_exp['experience']), "r--", alpha=0.8, linewidth=2, label='Trend')
    ax1.legend()
    
    # Experience vs Salary
    df_salary = df_exp[df_exp['salary'] > 0]
    if len(df_salary) > 0:
        ax2.scatter(df_salary['experience'], df_salary['salary'],
                   alpha=0.6, color='steelblue', s=80, edgecolors='darkblue', linewidth=0.5)
        ax2.set_xlabel('Years of Experience Required', fontsize=12, fontweight='bold')
        ax2.set_ylabel('Annual Salary (USD)', fontsize=12, fontweight='bold')
        ax2.set_title('Salary vs Experience Level', fontsize=14, fontweight='bold')
        ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1000:.0f}K'))
        ax2.grid(True, alpha=0.3)
        
        # Add trend line
        z = np.polyfit(df_salary['experience'], df_salary['salary'], 1)
        p = np.poly1d(z)
        ax2.plot(df_salary['experience'], p(df_salary['experience']), "r--", alpha=0.8, linewidth=2, label='Trend')
        ax2.legend()
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/experience_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"   ✅ Saved: experience_analysis.png")

def create_location_chart(jobs, output_dir):
    """Create bar chart of top hiring locations"""
    location_counts = Counter([job.location for job in jobs if job.location])
    top_locations = location_counts.most_common(10)
    
    if not top_locations:
        print("   ⚠️  No location data found")
        return
    
    locations, counts = zip(*top_locations)
    
    plt.figure(figsize=(14, 10))
    colors = sns.color_palette("coolwarm", len(locations))
    plt.barh(range(len(locations)), counts, color=colors, edgecolor='black', linewidth=0.5)
    plt.yticks(range(len(locations)), locations, fontsize=12)
    plt.xlabel('Number of Job Postings', fontsize=13, fontweight='bold')
    plt.title('Top 10 Locations for Tech Jobs', fontsize=16, fontweight='bold', pad=20)
    plt.gca().invert_yaxis()
    
    # Add value labels
    for i, count in enumerate(counts):
        plt.text(count + 0.5, i, str(count), va='center', fontsize=11, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/top_locations.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"   ✅ Saved: top_locations.png")

def create_tech_stack_heatmap(jobs, output_dir):
    """Create heatmap showing tech stack demand"""
    
    # Define tech categories - all same length for consistent matrix
    categories = {
        'Languages': ['Python', 'JavaScript', 'Java', 'TypeScript', 'Go', 'Rust'],
        'Frontend': ['React', 'Vue', 'Angular', 'HTML', 'CSS', 'Next.js'],
        'Backend': ['Node.js', 'Django', 'Flask', 'Spring', 'Express', 'FastAPI'],
        'Database': ['PostgreSQL', 'MongoDB', 'MySQL', 'Redis', 'Elasticsearch', 'DynamoDB'],
        'Cloud': ['AWS', 'Azure', 'GCP', 'Docker', 'Kubernetes', 'Terraform']
    }
    
    # Count occurrences for each skill
    matrix_data = []
    for cat_name, cat_skills in categories.items():
        row = []
        for skill in cat_skills:
            count = sum(1 for job in jobs if job.required_skills and skill in job.required_skills)
            row.append(count)
        matrix_data.append(row)
    
    # Create DataFrame for easier manipulation
    import pandas as pd
    df = pd.DataFrame(matrix_data, 
                      index=list(categories.keys()),
                      columns=range(6))  # 6 skills per category
    
    plt.figure(figsize=(14, 8))
    
    # Create skill labels with category prefix
    skill_labels = []
    for cat_name, cat_skills in categories.items():
        skill_labels.extend(cat_skills)
    
    # Use a flattened version for better visualization
    flat_data = []
    flat_labels = []
    for cat_name, cat_skills in categories.items():
        for skill in cat_skills:
            count = sum(1 for job in jobs if job.required_skills and skill in job.required_skills)
            flat_data.append([count])
            flat_labels.append(f"{skill}")
    
    # Create simplified heatmap with just one column per skill
    sns.heatmap(
        np.array(flat_data[:30]).reshape(5, 6),  # Top 30 skills in 5x6 grid
        xticklabels=[categories[cat][i] for cat in categories for i in range(6)][:30],
        yticklabels=list(categories.keys()),
        annot=True,
        fmt='d',
        cmap='YlGnBu',
        cbar_kws={'label': 'Job Postings'},
        linewidths=1,
        linecolor='white'
    )
    
    plt.title('Tech Stack Demand Heatmap', fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Technologies', fontsize=12, fontweight='bold')
    plt.ylabel('Category', fontsize=12, fontweight='bold')
    plt.xticks(rotation=45, ha='right', fontsize=9)
    plt.yticks(rotation=0, fontsize=11)
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/tech_stack_heatmap.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"   ✅ Saved: tech_stack_heatmap.png")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Create visualizations")
    parser.add_argument("--output", default="./visualizations", help="Output directory")
    
    args = parser.parse_args()
    
    visualize_all_trends(args.output)
