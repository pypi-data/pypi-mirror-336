#!/usr/bin/env python3

import argparse
import os
import yaml
import sys
import re
from colorama import init, Fore, Style

# Initialize colorama for cross-platform colored terminal output
init()

def validate_singularity_compose(singularity_compose_path, docker_compose_path=None):
    """
    Validate a singularity-compose.yml file and provide guidance on potential issues.
    
    Args:
        singularity_compose_path: Path to the singularity-compose.yml file
        docker_compose_path: Optional path to the original docker-compose.yml for comparison
    """
    # Read the singularity-compose.yml file
    try:
        with open(singularity_compose_path, 'r') as f:
            singularity_compose = yaml.safe_load(f)
    except Exception as e:
        print(f"{Fore.RED}Error reading singularity-compose file: {e}{Style.RESET_ALL}")
        return False
    
    # Read the docker-compose.yml file if provided
    docker_compose = None
    if docker_compose_path and os.path.exists(docker_compose_path):
        try:
            with open(docker_compose_path, 'r') as f:
                docker_compose = yaml.safe_load(f)
        except Exception as e:
            print(f"{Fore.YELLOW}Warning: Could not read docker-compose file: {e}{Style.RESET_ALL}")
    
    # Check basic structure
    if 'instances' not in singularity_compose:
        print(f"{Fore.RED}Error: No 'instances' section found in singularity-compose file{Style.RESET_ALL}")
        return False
    
    # Check for empty instances
    if not singularity_compose['instances']:
        print(f"{Fore.RED}Error: No instances defined in singularity-compose file{Style.RESET_ALL}")
        return False
    
    print(f"{Fore.GREEN}Validating Singularity Compose file...{Style.RESET_ALL}")
    print(f"Found {len(singularity_compose['instances'])} instances to validate.\n")
    
    issues_found = 0
    warnings_found = 0
    
    # Validate each instance
    for instance_name, instance_config in singularity_compose['instances'].items():
        print(f"{Fore.CYAN}Checking instance: {instance_name}{Style.RESET_ALL}")
        
        # Check container image
        if 'container' not in instance_config:
            print(f"{Fore.RED}  Error: No 'container' specified for {instance_name}{Style.RESET_ALL}")
            issues_found += 1
        elif instance_config['container'].startswith('#'):
            print(f"{Fore.RED}  Error: Container for {instance_name} needs manual attention: {instance_config['container']}{Style.RESET_ALL}")
            print(f"  {Fore.YELLOW}Suggestion: Create a Singularity definition file and build a .sif image{Style.RESET_ALL}")
            issues_found += 1
        
        # Check for privileged mode or root requirements
        if docker_compose and 'services' in docker_compose and instance_name in docker_compose['services']:
            docker_service = docker_compose['services'][instance_name]
            
            # Check for privileged mode
            if 'privileged' in docker_service and docker_service['privileged']:
                print(f"{Fore.YELLOW}  Warning: Service {instance_name} uses privileged mode in Docker{Style.RESET_ALL}")
                print(f"  {Fore.YELLOW}Suggestion: You may need to run Singularity with --privileged or use the 'privileged' option{Style.RESET_ALL}")
                warnings_found += 1
            
            # Check for user directive
            if 'user' in docker_service:
                print(f"{Fore.YELLOW}  Warning: Service {instance_name} specifies user '{docker_service['user']}' in Docker{Style.RESET_ALL}")
                print(f"  {Fore.YELLOW}Suggestion: Singularity's user namespace works differently; you may need to adjust your approach{Style.RESET_ALL}")
                warnings_found += 1
        
        # Check volumes
        if 'volumes' in instance_config:
            for volume in instance_config['volumes']:
                if ':' in volume:
                    host_path = volume.split(':')[0]
                    if not os.path.exists(host_path) and not host_path.startswith('/'):
                        print(f"{Fore.YELLOW}  Warning: Volume path '{host_path}' may not exist or is relative{Style.RESET_ALL}")
                        print(f"  {Fore.YELLOW}Suggestion: Ensure the path exists and consider using absolute paths{Style.RESET_ALL}")
                        warnings_found += 1
        
        # Check for networking issues
        if 'ports' in instance_config:
            print(f"{Fore.YELLOW}  Note: Singularity networking differs from Docker. Verify port mappings work as expected.{Style.RESET_ALL}")
            warnings_found += 1
        
        # Check for environment variables that might cause issues
        if 'environment' in instance_config:
            env_vars = instance_config['environment']
            for key, value in env_vars.items():
                if key.lower() in ['home', 'path', 'user', 'shell']:
                    print(f"{Fore.YELLOW}  Warning: Environment variable '{key}' might conflict with Singularity's environment{Style.RESET_ALL}")
                    warnings_found += 1
        
        # Check for unsupported Docker features
        if docker_compose and 'services' in docker_compose and instance_name in docker_compose['services']:
            docker_service = docker_compose['services'][instance_name]
            
            unsupported_features = []
            if 'deploy' in docker_service:
                unsupported_features.append('deploy')
            if 'healthcheck' in docker_service:
                unsupported_features.append('healthcheck')
            if 'secrets' in docker_service:
                unsupported_features.append('secrets')
            if 'configs' in docker_service:
                unsupported_features.append('configs')
            
            if unsupported_features:
                print(f"{Fore.YELLOW}  Warning: Docker service uses features not directly supported in Singularity: {', '.join(unsupported_features)}{Style.RESET_ALL}")
                print(f"  {Fore.YELLOW}Suggestion: These features need alternative implementations in Singularity{Style.RESET_ALL}")
                warnings_found += 1
        
        print("")  # Add a blank line between instances
    
    # Check for Docker networks that need attention
    if docker_compose and 'networks' in docker_compose:
        print(f"{Fore.YELLOW}Warning: Docker Compose defines custom networks that need manual configuration in Singularity{Style.RESET_ALL}")
        print(f"  {Fore.YELLOW}Suggestion: Review Singularity networking options and adjust your configuration{Style.RESET_ALL}")
        warnings_found += 1
    
    # Check for Docker volumes that need attention
    if docker_compose and 'volumes' in docker_compose and isinstance(docker_compose['volumes'], dict):
        print(f"{Fore.YELLOW}Warning: Docker Compose defines named volumes that need manual configuration in Singularity{Style.RESET_ALL}")
        print(f"  {Fore.YELLOW}Suggestion: Create appropriate directories on the host and update volume mappings{Style.RESET_ALL}")
        warnings_found += 1
    
    # Summary
    print(f"\n{Fore.GREEN}Validation Summary:{Style.RESET_ALL}")
    print(f"  Instances checked: {len(singularity_compose['instances'])}")
    print(f"  {Fore.RED}Issues found: {issues_found}{Style.RESET_ALL}")
    print(f"  {Fore.YELLOW}Warnings found: {warnings_found}{Style.RESET_ALL}")
    
    if issues_found == 0 and warnings_found == 0:
        print(f"\n{Fore.GREEN}No issues detected! Your Singularity Compose file looks good.{Style.RESET_ALL}")
        print("Note: This tool cannot catch all potential issues. Test your configuration thoroughly.")
    else:
        print(f"\n{Fore.YELLOW}Please address the issues and warnings above before running your Singularity Compose file.{Style.RESET_ALL}")
        
        # Provide general guidance
        print(f"\n{Fore.CYAN}General Guidance for Singularity Conversion:{Style.RESET_ALL}")
        print("1. Singularity containers run with user permissions, not as root by default")
        print("2. Consider using Singularity definition files for custom container builds")
        print("3. Test each container individually before running the full compose setup")
        print("4. Review Singularity documentation for networking and volume mounting specifics")
        print("5. Some Docker features may require external scripts or different approaches in Singularity")
    
    return issues_found == 0

def main():
    parser = argparse.ArgumentParser(description='Validate singularity-compose.yml and provide guidance')
    parser.add_argument('input', help='Path to singularity-compose.yml file')
    parser.add_argument('-d', '--docker', help='Path to original docker-compose.yml file for comparison')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.input):
        print(f"{Fore.RED}Error: Input file {args.input} does not exist{Style.RESET_ALL}")
        sys.exit(1)
    
    success = validate_singularity_compose(args.input, args.docker)
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()
